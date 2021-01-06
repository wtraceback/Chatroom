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
    });

    // register form
    $('.register.ui.form').form({
        inline: true,
        on: 'blur',
        fields: {
            username: {
                identifier: 'username',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your username'
                    }, {
                        type: 'maxLength[64]',
                        prompt: 'Your username must be not more than {ruleValue} characters'
                    }
                ]
            },
            email: {
                identifier: 'email',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter you e-mail'
                    }, {
                        type: 'email',
                        prompt: 'Please enter a valid e-mail'
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
            password2: {
                identifier: 'password2',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your password'
                    }, {
                        type: 'minLength[6]',
                        prompt: 'Your password must be at least 6 characters'
                    }, {
                        type: 'match[password]',
                        prompt: 'Your confirm password must be match the value of the password field'
                    }
                ]
            }
        }
    });
});
