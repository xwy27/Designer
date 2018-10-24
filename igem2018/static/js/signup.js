$(document).ready(function () {
    
    $('.ui.form')
        .form({
            fields: { 
                username: {
                    identifier  : 'regex',
                    rules: [
                      {
                        type   : 'regExp[/^[a-zA-Z0-9]+$/]',
                        prompt : 'Username can only contain alphas and digits.'
                      }
                    ]
                  },
                email: ['email', 'empty'],
                password: ['minLength[6]', 'empty'],
                password2: ['match[password]'],
                org: ['empty'],
                igem: ['email']
            }
        });

    $('#signup-button')
        .on('click', function () {
            var pattern = new RegExp('^[a-zA-Z0-9]+$');
            if (!pattern.test($('#username').val())) {
                $('.error.message>.list').html('<li>Username can only contain alphas and digits.</li>');
                $('.error.message').show();
                return;
            }
            $('.error.message').hide();
            $('.ui.form').form('submit');
        });
    $('#login-button')
        .on('click', function () {
            window.location.href = '/login';
        });

    $('#policy').on('click', () => {
        $('#policy-modal').modal('show');
    });
    $('#cancel').on('click', () => {
        $('#policy-modal').modal('hide');
    });

})