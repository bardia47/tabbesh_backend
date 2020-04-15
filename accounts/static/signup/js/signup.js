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


function check() {
	if (!$('#username-check-alert').is(':visible') &&
		!$('#firstname-check-alert').is(':visible') &&
		!$('#lastname-check-alert').is(':visible')) {
		return true;
	}
	return false;
}