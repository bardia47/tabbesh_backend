$(document).ready(function () {

    // Profile image valid check 
    $("#file").on('change', function () {
        readURL(this);
    });
    // function to read input file
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                let image = new Image();
                image.src = e.target.result;
                let file = document.getElementById('file').files.item(0)
                let file_size = file.size / (1024 * 1024)
                image.onload = function () {
                    if ((this.width / this.height >= 1.25 || this.height / this.width >= 1.25) || file_size > 1) {
                        document.getElementById('avatar_form').reset();
                        $("#modal").modal();
                        $("#modal-body").text("طول و عرض عکس باید یکسان و سایز تصویر کم تر از 1 مگابایت باشد.")
                    } else {
                        $('.avatar').attr('src', e.target.result);
                    }
                }
            }

            reader.onerror = function () {
                $("#modal").modal();
                $("#modal-body").text("آپلود فایل به مشکل خورده است! لطفا دوباره تلاش کنید.")
            }

            reader.readAsDataURL(input.files[0]);

        }
    }

    //Check new password & coniform password equal
    $('#password2').on('keyup', function () {
        if ($('#password').val() == $('#password2').val() && $("#password2").is(":focus")) {
            $("#change-password-alert").hide()
        } else {
            $("#change-password-alert").show()
        }
    });

    // Check if click ثبت button the other inputs form not required
    $('#edit_profile').click(function () {
        $('[name="old_password"]').prop('required', false);
        $('#password').prop('required', false);
        $('#password2').prop('required', false);
    });

    // Check if click تغییر رمز عبور button the other inputs form not required
    $('#changePassword').click(function () {
        $('input').prop('required', false);
        $('select').prop('required', false);
    });


    // Check if click آپلود button the other inputs form not required
    $('[name="upload"]').click(function () {
        $('input').prop('required', false);
        $('select').prop('required', false);
        $('#file').prop('required', true);
    });


    // Check firstname contain persian character
    $('#first_name').on('keyup', function () {
        var p = /^[\u0600-\u06FF\s]+$/;
        if ((p.test($('#first_name').val()) || !$('#first_name').val())) {
            $('#name-check-alert').hide()
        } else {
            $('#name-check-alert').show()
        }
    });

    // Check lastname contain persian character
    $('#last_name').on('keyup', function () {
        var p = /^[\u0600-\u06FF\s]+$/;
        if ((p.test($('#last_name').val()) || !$('#last_name').val())) {
            $('#lastname-check-alert').hide()
        } else {
            $('#lastname-check-alert').show()
        }
    });

    // Username valid check
    $('#username').on('keyup', function () {
        var p = /^[a-zA-Z0-9]+$/;
        if (p.test($('#username').val())) {
            $('#username-check-alert').hide();
        } else {
            $('#username-check-alert').show();
        }
    });
});
