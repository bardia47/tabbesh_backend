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

// username valid check
$("#username").on("keyup", function () {
    let p = /^[a-zA-Z0-9]+$/;
    let username = $("#username");
    username.val(persianToEnglishNumbers(username.val()));
    if (p.test(username.val()) || !username.val()) {
        $("#usernameCheckAlert").hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $("#usernameCheckAlert").show();
        $("#submit").prop("disabled", true);

    }
});

// phone number validation check
$("#phoneNumber").on("keyup", function () {
    let phoneNumberRegEx = /^(\+98|0)?9\d{9}$/;
    let phoneNumber = $("#phoneNumber");
    phoneNumber.val(persianToEnglishNumbers(phoneNumber.val()));
    if (phoneNumberRegEx.test(phoneNumber.val()) || !phoneNumber.val()) {
        $("#phoneNumberCheckAlert").hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $("#phoneNumberCheckAlert").show();
        $("#submit").prop("disabled", true);

    }
});

function check() {
    return !$("#usernameCheckAlert").is(":visible") &&
        !$("#firstNameCheckAlert").is(":visible") &&
        !$("#lastNameCheckAlert").is(":visible") &&
        !$("#phoneNumberCheckAlert").is(":visible");

}

// change +98 & 09 to 9
$("#formSignUp").submit(function () {
    let phoneNumber = $("#phoneNumber");
    if (phoneNumber.val().startsWith("0")) {
        phoneNumber.val(phoneNumber.val().slice(1))
    } else if (phoneNumber.startsWith("+98")) {
        phoneNumber.val(phoneNumber.val().slice(3))
    }
});