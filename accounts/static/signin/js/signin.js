$(function () {
    $("#signInForm").submit(function () {
        let username = $("#username");
        let password = $("#password");
        username.val(persianToEnglishNumbers(username.val()));
        password.val(persianToEnglishNumbers(password.val()));
        let phoneNumberRegEx = /^0?9\d{9}$/;
        if (phoneNumberRegEx.test(username.val())) {
            // change phone number to standard format
            if (username.val().startsWith("0")) {
                username.val(username.val().slice(1))
            }
        }
    });

    let sendForgetPasswordMessage = false;
    $('#forgetPasswordTag').click(function () {
        // for forget password
        // $('#forgetPasswordModal').modal('show')
        window.Raychat.toggle();
        setTimeout(
            function () {
                if (!sendForgetPasswordMessage) {
                    window.Raychat.sendOfflineMessage('در صورت فراموشی رمز، نام و نام خانوادگی و شماره تلفن را در اینجا وارد کنید تا همکاران ما رمز عبور جدید را ارسال کنند.');
                    window.Raychat.sendOfflineMessage('مثال: محمد محمدی 09123456789');
                    sendForgetPasswordMessage = true;
                }
            }, 2000);
    });
});
