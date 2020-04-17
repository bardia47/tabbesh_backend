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