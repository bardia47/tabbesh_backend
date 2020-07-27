// convert persian and arabic numbers to english numbers
function persianToEnglishNumbers(convertedNumbers) {
    const persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g]
    const arabicNumbers = [/٠/g, /١/g, /٢/g, /٣/g, /٤/g, /٥/g, /٦/g, /٧/g, /٨/g, /٩/g]
    if (typeof convertedNumbers === 'string') {
        for (let i = 0; i < 10; i++) {
            convertedNumbers = convertedNumbers.replace(persianNumbers[i], i).replace(arabicNumbers[i], i);
        }
    }
    return convertedNumbers;
};


// Check firstname contain persian character
$('#first_name').on('keyup', function () {
    let p = /^[\u0600-\u06FF\s]+$/;
    if (p.test($('#first_name').val()) || !$('#first_name').val()) {
        $('#firstname-check-alert').hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $('#firstname-check-alert').show();
        $("#submit").prop("disabled", true);

    }
});


// Check lastname contain persian character
$('#last_name').on('keyup', function () {
    let p = /^[\u0600-\u06FF\s]+$/;
    if (p.test($('#last_name').val()) || !$('#last_name').val()) {
        $('#lastname-check-alert').hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $('#lastname-check-alert').show();
        $("#submit").prop("disabled", true);

    }
});

// Username valid check
$('#username').on('keyup', function () {
    let p = /^[a-zA-Z0-9]+$/;
    if (p.test($('#username').val()) || !$('#username').val()) {
        $('#username-check-alert').hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $('#username-check-alert').show();
        $("#submit").prop("disabled", true);

    }
});

// phone number validation check
$('#phoneNumber').on("keyup", function () {
    let phoneNumberRegEx = /^(\+98|0)?9\d{9}$/g;
    $("#phoneNumber").val(persianToEnglishNumbers($("#phoneNumber").val()))
	console.log($("#phoneNumber").val())
    if (phoneNumberRegEx.test($("#phoneNumber").val()) || !$("#phoneNumber").val()) {
        $("#phoneNumberCheckAlert").hide();
        if (check()) {
            $("#submit").prop("disabled", false);
        }
    } else {
        $('#phoneNumberCheckAlert').show();
        $("#submit").prop("disabled", true);

    }
});

function check() {
    if (!$('#phoneNumberCheckAlert').is(':visible') &&
        !$('#firstname-check-alert').is(':visible') &&
        !$('#lastname-check-alert').is(':visible') &&
        !$('#lastname-check-alert').is(':visible')) {
        return true;
    }
    return false;
}

// change +98 & 09 to 9
$("#formSignUp").submit(function (event) {
    const phoneNubmer = $("#phoneNumber").val()
    if (phoneNubmer.startsWith("0")) {
        $("#phoneNumber").val(phoneNubmer.slice(1))
    } else if (phoneNubmer.startsWith("+98")) {
        $("#phoneNumber").val(phoneNubmer.slice(3))
    }
});


document.addEventListener("DOMContentLoaded", function () {
    let elements = document.getElementsByTagName("INPUT");
    for (let i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function (e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity("این مورد اجباری می باشد.");
            }
        };
        elements[i].oninput = function (e) {
            e.target.setCustomValidity("");
        };
    }
});


document.addEventListener("DOMContentLoaded", function () {
    let elements = document.getElementsByTagName("SELECT");
    for (let i = 0; i < elements.length; i++) {
        elements[i].oninvalid = function (e) {
            e.target.setCustomValidity("");
            if (!e.target.validity.valid) {
                e.target.setCustomValidity("لطفا یکی از موارد را انتخاب کنید.");
            }
        };
        elements[i].oninput = function (e) {
            e.target.setCustomValidity("");
        };
    }
});