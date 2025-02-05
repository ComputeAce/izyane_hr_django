console.log("Password change");

$(document).ready(function () {
    function toggleSubmitButton() {
        const isCurrentPasswordValid = $('#password-feedback').text() === 'Password is correct';
        const newPassword = $('#new_password').val().trim();
        const confirmPassword = $('#confirm_new_password').val().trim();
        const doPasswordsMatch = newPassword === confirmPassword && newPassword !== '';

        const shouldEnable = isCurrentPasswordValid && doPasswordsMatch;

        $('#submitBtn').prop('disabled', !shouldEnable);

    
        if (!doPasswordsMatch && newPassword !== '' && confirmPassword !== '') {
            $('#password-match-feedback').text('Passwords do not match').css('color', 'red');
        } else {
            $('#password-match-feedback').text('');
        }
    }

    $('#current_password').on('keyup', function () {
        var currentPassword = $(this).val();

        if (currentPassword.trim() !== '') {
            $.ajax({
                url: '/update_password/',  
                type: 'POST',
                data: {
                    'current_password': currentPassword,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    if (response.status === 'success') {
                        $('#password-feedback').text('Password is correct').css('color', 'green');
                        $('#new_password').closest('.single-form').show();
                        $('#confirm_new_password').closest('.single-form').show();
                        toggleSubmitButton();
                    } else if (response.status === 'error') {
                        $('#password-feedback').text('Invalid password').css('color', 'red');
                        $('#new_password').closest('.single-form').hide();
                        $('#confirm_new_password').closest('.single-form').hide();
                        toggleSubmitButton();
                    }
                },
                error: function (xhr, status, error) {
                    $('#password-feedback').text('An error occurred').css('color', 'red');
                    $('#new_password').closest('.single-form').hide();
                    $('#confirm_new_password').closest('.single-form').hide();
                    toggleSubmitButton();
                }
            });
        } else {
            $('#password-feedback').text('');
            $('#new_password').closest('.single-form').hide();
            $('#confirm_new_password').closest('.single-form').hide();
            toggleSubmitButton();
        }
    });

    $('#new_password, #confirm_new_password').on('keyup', function () {
        toggleSubmitButton();
    });


    $('#new_password').closest('.single-form').hide();
    $('#confirm_new_password').closest('.single-form').hide();
    $('#submitBtn').prop('disabled', true);
});


$(document).ready(function () {
    $('#submitBtn').on('click', function (event) {
        event.preventDefault();  
        
        const newPassword = $('#new_password').val().trim();  
        
        $.ajax({
            url: '/submit_change_password/',  
            type: 'POST',
            data: {
                'new_password': newPassword,  
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(), 
            },
            success: function (response) {
                console.log(response.message);  
                
        
                if (response.message === 'Password updated successfully') {
                   
                    $('#password-feedback').html(
                        '<p style="font-size: 18px; font-weight: bold; color: green;">Password has been changed successfully.</p>' +
                        '<p style="font-size: 16px; color: orange;">You will be logged out shortly.</p>'
                    );
                    
                  
                    setTimeout(function () {
                        window.location.href = '/logout_user/';  
                    }, 10000);  
                }
            },
            error: function (xhr, status, error) {
                console.log("Error:", error);  
                $('#password-feedback').text('An error occurred. Please try again.').css('color', 'red');
            }
        });
    });
});


