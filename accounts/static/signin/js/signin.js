$('#submit').click(function () {
    var p = /^[0]\d+$/;
    if (p.test($('#username').val())) {
        $('#username').val($('#username').val().substring(1, $('#username').val().length));
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


$('#forgetPasswordTag').click(function () {

    $('#forgetPasswordModal').modal('show')
});