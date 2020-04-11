$(document).ready(function () {

    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.avatar').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }


    $(".file-upload").on('change', function () {
        readURL(this);
    });
});

//Check new password & coniform password equal
$('#password, #password2').on('keyup', function () {
  if ($('#password').val() == $('#password2').val()) {
	  $('#password_message').html('');
	  $("#changePassword").prop("disabled",false);
  } else {
	  $('#password_message').html('تکرار رمز صحیح نمیباشد');
	    $("#changePassword").prop("disabled",true);

	  }
});

// Check if click ثبت button the other inputs form not required
$('#edit_profile').click(function () {
    $('[name="old_password"]').prop('required',false);
    $('#password').prop('required',false);
    $('#password2').prop('required',false);
 });

 // Check if click تغییر رمز عبور button the other inputs form not required
$('#changePassword').click(function () {
    $('input').prop('required',false);
    $('select').prop('required',false);
 });

  // Check if click آپلود button the other inputs form not required
  $('[name="upload"]').click(function () {
    $('input').prop('required',false);
    $('select').prop('required',false);
    $('#file').prop('required',true);
 });
