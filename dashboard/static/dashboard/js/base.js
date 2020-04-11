$(document).ready(function () {
    $("#sidebarCollapse").click(function () {
        $("#sidebar").toggleClass('active');
        $("#content").toggleClass('active');
    });
});

$('#contact_us_img').click(function () {
    $("#contact_us_content").animate({ width: 'toggle' }, "slow");
});