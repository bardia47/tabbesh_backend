$('#submit').click(function() {
	var p = /^[0]\d+$/;
	if (p.test($('#username').val()) ) {
		$('#username').val($('#username').val().substring(1, $('#username').val().length));
	} 
});
