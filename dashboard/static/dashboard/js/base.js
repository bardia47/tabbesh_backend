$(document).ready(function () {
    $("#sidebarCollapse").click(function () {
        $("#sidebar").toggleClass('active');
        $("#content").toggleClass('active');
    });
});

// contact us pop up
$('#contact_us_img').click(function () {
    $("#contact_us_content").animate({
        width: 'toggle'
    }, "slow");
});

// remove sticky nav bar in mobile
$(window).resize(function () {
    if($(window).width() < 900){
        $('#nav').removeClass('sticky-top');
    }
    else{
        $('#nav').addClass('sticky-top');
    }
});