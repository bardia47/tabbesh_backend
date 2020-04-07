// $('#password, #password2').on('keyup', function () {
//   if ($('#password').val() == $('#password2').val()) {
// 	  $('#password_message').html('');
// 	  if (check())
// 	  {
// 	  $("#submit").prop("disabled",false);
// 	  }
//   } else {
// 	  $('#password_message').html('تکرار رمز صحیح نمیباشد');
// 	    $("#submit").prop("disabled",true);

// 	  }
// });
// Check firstname & lastname contain persian character
$('#first_name, #last_name').on('keyup', function () {
	var p = /^[\u0600-\u06FF\s]+$/;
	if ((p.test($('#first_name').val())|| !$('#first_name').val()) && (p.test($('#last_name').val()) || !$('#last_name').val())) {
		  $('#name_message').html('');
		  if (check())
		  {
		  $("#submit").prop("disabled",false);
		  }
	  } else {
		  $('#name_message').html('نام و نام خانوادگی باید فارسی باشند');
		    $("#submit").prop("disabled",true);

		  }
	});

$('#username').on('keyup', function () {
	var p = /^[a-zA-Z0-9]+$/;
	if (p.test($('#username').val())) {
		  $('#username_message').html('');
		  if (check())
			  {
			  $("#submit").prop("disabled",false);
			  }
	  } else {
		  $('#username_message').html('نام کاربری تنها باید شامل حروف  و اعداد انگلیسی باشد');
		    $("#submit").prop("disabled",true);

		  }
	});


function check() {
	var username=document.getElementById('username_message').innerHTML;
	var name=document.getElementById('name_message').innerHTML;
	if (username=="" && name==""  ) {
		return true;
	}
	return false;
	}


