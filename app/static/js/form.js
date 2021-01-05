$(document).ready(function() {
    // login form
    $('.login.ui.form').form({
        fields: {
            username: {
                identifier: 'username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your username'
                    }
                ]
            },
            password: {
                identifier: 'password',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your password'
                    }, {
                        type: 'minLength[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }
                ]
            },
        }
    })
});
