import os
from flask import abort, redirect, url_for, flash
from flask_login import current_user, login_user
from app import oauth2, db
from app.models import User
from app.oauth import oauth_bp


github = oauth2.remote_app(
    name='github',
    consumer_key=os.getenv('GITHUB_CLIENT_ID'),
    consumer_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params={'scope': 'user'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

providers = {
    'github': github
}

profile_endpoints = {
    'github': 'user'
}

def get_social_profile(provider, access_token):
    # 通过令牌，去请求数据  get() 或 post() 使用某种 HTTP 方法来请求数据。
    profile_endpoint = profile_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=access_token)

    username = response.data.get('name')
    email = response.data.get('email')
    github = response.data.get('html_url')
    website = response.data.get('blog')
    bio = response.data.get('bio')

    return username, email, github, website, bio


@oauth_bp.route('/login/<provider_name>')
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)

    if current_user.is_authenticated:
        redirect(url_for('chat.index'))

    callback = url_for('oauth.oauth_callback', provider_name=provider_name, _external=True)

    # 登录/获取授权码
    return providers[provider_name].authorize(callback=callback)


@oauth_bp.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    if provider_name not in providers.keys():
        abort(404)

    provider = providers[provider_name]
    response = provider.authorized_response()

    if response is None:
        flash('Access denied, please try again.')
        return redirect(url_for('auth.login'))

    # 获取令牌
    access_token = response.get('access_token')
    username, email, github, website, bio = get_social_profile(provider, access_token)

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(username=username, email=email, github=github, website=website, bio=bio)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for('chat.index'))
