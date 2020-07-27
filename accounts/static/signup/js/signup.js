// check first name & last name contains persian character
$("#first-name , #last-name").on("keyup", function () {
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
        $("#username-check-alert").hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $("#username-check-alert").show();
        $("#submit").prop("disabled", true);

    }
});

// phone number validation check
$("#phone-number").on("keyup", function () {
    let phoneNumberRegEx = /^(\+98|0)?9\d{9}$/;
    let phoneNumber = $("#phone-number");
    phoneNumber.val(persianToEnglishNumbers(phoneNumber.val()));
    if (phoneNumberRegEx.test(phoneNumber.val()) || !phoneNumber.val()) {
        $("#phone-number-check-alert").hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $("#phone-number-check-alert").show();
        $("#submit").prop("disabled", true);

    }
});

function check() {
    return !$("#username-check-alert").is(":visible") &&
        !$("#first-name-check-alert").is(":visible") &&
        !$("#last-name-check-alert").is(":visible") &&
        !$("#phone-number-check-alert").is(":visible");

}

// change +98 & 09 to 9
$("#formSignUp").submit(function () {
    let phoneNumber = $("#phone-number");
    if (phoneNumber.val().startsWith("0")) {
        phoneNumber.val(phoneNumber.val().slice(1))
    } else if (phoneNumber.startsWith("+98")) {
        phoneNumber.val(phoneNumber.val().slice(3))
    }
});