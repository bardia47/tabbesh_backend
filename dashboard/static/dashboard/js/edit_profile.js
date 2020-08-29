function activeMenu() {
    let menuTemplate = `
    <hr>
    <div id="editProfileMenu" class="row sidebar-menu active-menu">
        <img src="/static/home/images/icons/edit-pofile-menu.svg" alt="edit profile menu">
        <a href="">تغییر پروفایل</a>
    </div>
    `;
    $("#sidebarMenus").append(menuTemplate);
}


$(function () {

    // active menu
    activeMenu();

    // checkout hint with ray chat
    let checkoutStatus = false;
    $("#checkout").click(function (e) {
        e.preventDefault();
        window.addEventListener('raychat_ready', function (ets) {
            if (!checkoutStatus) {
                window.Raychat.sendOfflineMessage('با سلام و از همکاری شما در تابش ممنونیم 🌹');
                window.Raychat.sendOfflineMessage('در صورت تمایل به نقد کردن اعتبار خود نام و نام خانوادگی و شماره تلفن خود را در این مکان ارسال کنید، تا همکاران ما در اسرع وقت با شما تماس بگیرند.');
                checkoutStatus = true;
            }
        });
        window.Raychat.toggle();
    });

    // Profile image valid check
    profileCheck();

    // check first name & last name contains persian character
    $("#firstName , #lastName").on("keyup", function () {
        let p = /^[\u0600-\u06FF\s]+$/;
        if (p.test($(this).val()) || !$(this).val()) {
            $($(this).siblings("small")).hide();
            if (checkEditProfile()) {
                $("#editProfileSubmit").prop("disabled", false);
            }
        } else {
            $($(this).siblings("small")).show();
            $("#editProfileSubmit").prop("disabled", true);
        }
    });

    // Username valid check
    $('#username').on('keyup', function () {
        let p = /^[a-zA-Z0-9]+$/;
        let username = $("#username");
        username.val(persianToEnglishNumbers(username.val()));
        if (p.test(username.val())) {
            $('#usernameAlert').hide();
            if (checkEditProfile()) {
                $("#editProfileSubmit").prop("disabled", false);
            }
        } else {
            $('#usernameAlert').show();
            $("#editProfileSubmit").prop("disabled", true);
        }
    });

    // national code validation
    $("#nationalCode").on('keyup', function () {
        let nationalCode = $("#nationalCode");
        nationalCode.val(persianToEnglishNumbers(nationalCode.val()));
        if (isValidIranianNationalCode(nationalCode.val())) {
            $("#nationalCodeAlert").hide();
            if (checkEditProfile()) {
                $("#editProfileSubmit").prop("disabled", false);
            }
        } else {
            $("#nationalCodeAlert").show();
            $("#editProfileSubmit").prop("disabled", true);
        }
    });


    function checkEditProfile() {
        return !$("#firstNameAlert").is(":visible") &&
            !$("#lastNameAlert").is(":visible") &&
            !$("#usernameAlert").is(":visible") &&
            !$("#nationalCodeAlert").is(":visible");
    }

    $("#changeProfile").submit(function () {
        // remove white space with trim
        let firstName = $("#firstName");
        let lastName = $("#lastName");
        firstName.val(firstName.val().trim());
        lastName.val(lastName.val().trim());
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
            $("#change-password-alert").hide();
            $("#changePasswordSubmit").prop("disabled", false);
        } else {
            $("#change-password-alert").show();
            $("#changePasswordSubmit").prop("disabled", true);
        }
    });

});


function profileCheck() {
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
                let file = document.getElementById('file').files.item(0);
                let file_size = file.size / (1024 * 1024);
                image.onload = function () {
                    if ((this.width / this.height >= 1.25 || this.height / this.width >= 1.25) || file_size > 1) {
                        document.getElementById('avatar_form').reset();
                        $("#modal").modal();
                        $("#modal-body").text("طول و عرض عکس باید یکسان و سایز تصویر کم تر از 1 مگابایت باشد.")
                    } else {
                        $('.avatar').attr('src', e.target.result);
                    }
                }
            };

            reader.onerror = function () {
                $("#modal").modal();
                $("#modal-body").text("آپلود فایل به مشکل خورده است! لطفا دوباره تلاش کنید.")
            };

            reader.readAsDataURL(input.files[0]);

        }
    };
}