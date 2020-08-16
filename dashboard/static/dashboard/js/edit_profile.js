$(document).ready(function () {

    // Profile image valid check
    $("#file").on('change', function () {
        readURL(this);
    });
    // function to read input file
    let readURL = function (input) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();
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
});

//Check new password & conform password equal
$('#conformPassword').on('keyup', function () {
    let oldPassword = $('#oldPassword'),
        newPassword = $('#newPassword'),
        conformPassword = $('#conformPassword');
    oldPassword.val(persianToEnglishNumbers(oldPassword.val()));
    newPassword.val(persianToEnglishNumbers(newPassword.val()));
    conformPassword.val(persianToEnglishNumbers(conformPassword.val()));
    if (newPassword.val() === conformPassword.val() && $("#conformPassword").is(":focus")) {
        $("#change-password-alert").hide()
    } else {
        $("#change-password-alert").show()
    }
});

// Check if click ثبت button the other inputs form not required
$('#edit_profile').click(function () {
    $('#oldPassword').prop('required', false);
    $('#newPassword').prop('required', false);
    $('#conformPassword').prop('required', false);
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


// check first name & last name contains persian character
$("#firstName , #lastName").on("keyup", function () {
    let p = /^[\u0600-\u06FF\s]+$/;
    if (p.test($(this).val()) || !$(this).val()) {
        $($(this).siblings("small")).hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $($(this).siblings("small")).show();
        $("#submit").prop("disabled", true);

    }
});

// Username valid check
$('#username').on('keyup', function () {
    let p = /^[a-zA-Z0-9]+$/;
    $('#username').val(persianToEnglishNumbers($('#username').val()));
    if (p.test($('#username').val())) {
        $('#username-check-alert').hide();
    } else {
        $('#username-check-alert').show();
    }
});

$('#national-code').on('keyup', function () {
    $('#national-code').val(persianToEnglishNumbers($('#national-code').val()));
    if (isValidIranianNationalCode($('#national-code').val())) {
        $('#national-code-check-alert').hide();
    } else {
        $('#national-code-check-alert').show();
    }
});


// Check valid iranian national code
function isValidIranianNationalCode(input) {
    if (!/^\d{10}$/.test(input))
        return false;

    var check = parseInt(input[9]);
    var sum = 0;
    var i;
    for (i = 0; i < 9; ++i) {
        sum += parseInt(input[i]) * (10 - i);
    }
    sum %= 11;

    return (sum < 2 && check == sum) || (sum >= 2 && check + sum == 11);
}

$("#changeProfile").submit(function () {
    // remove white space with trim
    let firstName = $("#firstName");
    let lastName = $("#lastName");
    firstName.val(firstName.trim());
    lastName.val(lastName.trim());
});