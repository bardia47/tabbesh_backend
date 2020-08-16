$("#sign-in-form").submit(function () {
    let username = $("#username");
    let password = $("#password");
    username.val(persianToEnglishNumbers(username.val()));
    password.val(persianToEnglishNumbers(password.val()));
    let phoneNumberRegEx = /^(\+98|0)?9\d{9}$/;
    if (phoneNumberRegEx.test(username.val())) {
        // change phone number to standard format
        if (username.val().startsWith("0")) {
            username.val(username.val().slice(1))
        } else if (username.startsWith("+98")) {
            username.val(username.val().slice(3))
        }
    }
});


$('#forgetPasswordTag').click(function () {

    $('#forgetPasswordModal').modal('show')
});