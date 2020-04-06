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
$('#password, #password2').on('keyup', function () {
  if ($('#password').val() == $('#password2').val()) {
	  $('#password_message').html('');
	  $("#changePassword").prop("disabled",false);
  } else {
	  $('#password_message').html('تکرار رمز صحیح نمیباشد');
	    $("#changePassword").prop("disabled",true);

	  }
});

