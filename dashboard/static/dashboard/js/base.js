// Check page is loading or load 
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready())
} else {
    ready()
}


function ready() {
    $(document).ready(function () {
        $("#sidebarCollapse").click(function () {
            $("#sidebar").toggleClass('active');
            $("#content").toggleClass('active');
            if ($(window).width() < 768) {
                $("#nav-menu").toggleClass('navbar-mobile-view');
                $("#sidebar").toggleClass('mobile');
                $("#nav-items").toggleClass('flex-row-reverse');
            }
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
        if ($(window).width() < 768) {
            $('#nav').removeClass('sticky-top');
        } else {
            $('#nav').addClass('sticky-top');
        }
    });

}