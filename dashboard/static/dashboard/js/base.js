$(document).ready(function () {
    $("#sidebarCollapse").click(function () {
        $("#sidebar").toggleClass('active');
        $("#content").toggleClass('active');
    });
});