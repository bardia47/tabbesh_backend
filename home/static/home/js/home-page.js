$(function () {
    scrollAnimations();
    teacherListAjax();
    homeCounter();
    bestSellerAjax();
    fullDiscountAjax();
    supportAjax();
    $("#searchButton").on("click", function () {
        if ($("#searchInput").val().length != 0) searchAjax($("#searchInput").val());
    });

    // search when press enter
    $("#searchInput").on('keyup', function (e) {
        if (e.key === 'Enter' || e.keyCode === 13) {
            if ($("#searchInput").val().length != 0) searchAjax($("#searchInput").val());
        }
    });
    $('[data-toggle="tooltip"]').tooltip();

    commentsCarousel()
});


function homeCounter() {
    let firstTimeReach = false;
    $(window).scroll(function () {
        let hT = $('.desktop-counter').offset().top,
            hH = $('.desktop-counter').outerHeight(),
            wH = $(window).height(),
            wS = $(this).scrollTop();
        if (wS > (hT + hH - wH) && !firstTimeReach) {
            $.ajax({
                url: "/counter/",
                type: "GET",
                dataType: "json",
                cache: false,

                success: function (counters) {
                    $("#coursesCounter").animationCounter({
                        start: 0,
                        end: counters.course_counter,
                        step: 1,
                        delay: 200,
                    });
                    $("#studentsCounter").animationCounter({
                        start: 0,
                        end: counters.student_counter,
                        step: 1,
                        delay: 200,
                    });
                    $("#teachersCounter").animationCounter({
                        start: 0,
                        end: counters.teacher_counter,
                        step: 1,
                        delay: 200,
                    });
                },
                error: function () {
                    console.log("شمارنده با مشکل مواجه شد، دوباره امتحان کنید.")
                },
            });

            firstTimeReach = true;
        }
    });
}

function teacherListAjax() {
    $.ajax({
        url: "/all-teacher/",
        type: "GET",
        dataType: "json",
        cache: false,
        success: function (teachersList) {
            teacherListRender(teachersList)
        },
        error: function () {
            console.log("بارگذاری دبیران به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

function teacherListRender(teachersList) {
    let teachersTemplate = ``;
    $.each(teachersList, function (index, teacher) {
        let teacherTemplate = `
        <div class="mx-2">
            <div class="card">
                <img class="img-card mt-2" src="${teacher.avatar}" style="width: 150px !important; ; height: 150px !important;" alt="course image">
                <div class="card-body text-center">
                    <h4 class="text-nowrap">${teacher.get_full_name}</h4>
                    <h5 class="vazir-medium">${teacher.grade_choice}</h5>
                    <a href="/dashboard/shopping/?teacher=${teacher.id}" class="btn btn-secondary vazir-bold mt-2">مشاهده دروس</a>
                </div>
            </div>
        </div>
        `;
        teachersTemplate += teacherTemplate;
    });
    $("#teacherList").empty().append(teachersTemplate);
    owlCarouselInitial("#teacherList");
}


function bestSellerAjax() {
    $.ajax({
        url: "/best-selling-courses/",
        type: "GET",
        dataType: "json",
        cache: false,

        success: function (bestSellerCourses) {
            bestSellerRender(bestSellerCourses)
        },
        error: function () {
            console.log("بارگذاری پرفروش ترین دروس به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

function bestSellerRender(bestSellerCourses) {
    let coursesTemplate = ``;
    $.each(bestSellerCourses, function (index, course) {
        let courseTemplate = `
        <div class="mx-2">
            <div class="card">
                <img class="img-card" src="${course.image}" alt="course image">
                <div class="card-body text-center">
                    <h4 class="text-nowrap">${course.course_title}</h4>
                    <h5 class="vazir-medium">${course.teacher_full_name}</h5>
                    <a href="/dashboard/shopping/?grade=${course.id}" class="btn btn-secondary vazir-bold mt-2">خرید دوره</a>
                </div>
            </div>
        </div>
        `;
        coursesTemplate += courseTemplate;
    });
    $("#bestSellersCourse").empty().append(coursesTemplate);
    owlCarouselInitial("#bestSellersCourse");
}


function fullDiscountAjax() {
    $.ajax({
        url: "/most-discounted-courses/",
        type: "GET",
        dataType: "json",

        success: function (fullDiscountCourses, hel, xhr) {
            fullDiscountRender(fullDiscountCourses)
            console.log(xhr.getAllResponseHeaders());
        },
        error: function () {
            conslole.log("بارگذاری پرتخفیف ترین دروس به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

function fullDiscountRender(fullDiscountCourses) {
    let coursesTemplate = ``;
    $.each(fullDiscountCourses, function (index, course) {
        let courseTemplate = `
        <div class="mx-2 my-5">
            <div class="card">
                <div class="discount-red-circle">
                    <div class="discount-percent">
                       <p class="p-0 m-0 text-white">${course.percent} %</p>
                    </div>
                </div>
                <img class="img-card" src="${course.image}" alt="course discount">
                <div class="card-body text-center">
                    <h4>${course.course_title}</h4>
                    <h5 style="font-family: 'Vazir_medium';">${course.teacher_full_name}</h5>
                    <h5 class="h5">
                        <img class="d-inline" src="/static/home/images/home-page/icons/offer.svg" style="width: 30px !important; height: 30px">
                        با تخفیف 
                         ${course.discount_name}
                    </h5>
                    <a href="/dashboard/shopping/?grade=${course.id}" class="btn btn-secondary vazir-bold mt-2">خرید دوره</a>
                </div>
            </div>
        </div>
        `;
        coursesTemplate += courseTemplate;
    });
    $("#fullDiscountCourse").empty().append(coursesTemplate);
    owlCarouselInitial("#fullDiscountCourse");
}

function searchAjax(searchText) {
    $.ajax({
        url: "/search-home/",
        type: "GET",
        data: {
            "title": searchText
        },
        dataType: "json",
        cache: false,

        success: function (searchCourses) {
            if (searchCourses.length === 0) {
                $("#searchNotFound").show();
                $("#searchCourse").find(".owl-carousel").remove();
            } else {
                $("#searchNotFound").hide();
                searchRender(searchCourses)
            }
        },
        error: function () {
            console.log("جستجوی درس با خطا رو به رو شد! دوباره امتحان کنید.")
        },
    });
}

function searchRender(searchCourses) {
    let coursesTemplate = ``;
    $.each(searchCourses, function (index, course) {
        let courseTemplate = `
        <div class="mx-2">
            <div class="card">
                <img class="img-card" src="${course.image}" alt="course image">
                <div class="card-body text-center">
                    <h4 class="text-nowrap">${course.course_title}</h4>
                    <h5 class="vazir-medium">${course.teacher_full_name}</h5>
                    <a href="/dashboard/shopping/?grade=${course.id}" class="btn btn-secondary vazir-bold mt-2">خرید دوره</a>
                </div>
            </div>
        </div>
        `;
        coursesTemplate += courseTemplate;
    });
    let bestSellerCourse = $("#searchCourse");
    bestSellerCourse.find(".owl-carousel").remove();
    bestSellerCourse.append(`<div class="owl-carousel owl-theme"></div>`);
    bestSellerCourse.find(".owl-carousel").append(coursesTemplate);
    owlCarouselInitial(bestSellerCourse.find(".owl-carousel"));
}


function supportAjax() {
    $.ajax({
        url: "/support/",
        type: "GET",
        dataType: "json",
        cache: false,

        success: function (supports) {
            supportRender(supports)
        },
        error: function () {
            console.log("بارگذاری پشتیبانی به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

//for support
function supportRender(supports) {
    let supportsTemplate = ``;
    $.each(supports, function (index, support) {
        let supportTemplate = `
        <div class="mx-2">
            ${support.description}
        </div>       
        `;
        supportsTemplate += supportTemplate;
    });
    $("#supportList").empty().append(supportsTemplate);
    owlCarouselInitial("#supportList");
}


function owlCarouselInitial(carouselId) {
    //initial changes for carousels
    $(carouselId).owlCarousel({
        rtl: true,
        nav: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
            },
            720: {
                items: 3,
            }
        }
    });

    $(carouselId).find(".owl-prev").empty().append(`<img src="/static/home/images/home-page/icons/owl-prev.svg" width="40" height="40">`);
    $(carouselId).find(".owl-next").empty().append(`<img src="/static/home/images/home-page/icons/owl-next.svg" width="40" height="40">`);
}


function commentsCarousel() {
    //initial changes for carousels
    $("#commentsList").owlCarousel({
        loop: true,
        rtl: true,
        nav: true,
        items: 1,
    });

    $("#commentsList").find(".owl-prev").css("right", "30px").empty().append(`<img src="/static/home/images/home-page/icons/owl-prev.svg" width="40" height="40">`);
    $("#commentsList").find(".owl-next").css("left", "30px").empty().append(`<img src="/static/home/images/home-page/icons/owl-next.svg" width="40" height="40">`);
}

jQuery.event.special.touchstart = {
    setup: function (_, ns, handle) {
        if (ns.includes("noPreventDefault")) {
            this.addEventListener("touchstart", handle, {passive: false});
        } else {
            this.addEventListener("touchstart", handle, {passive: true});
        }
    }
};


function scrollAnimations() {
    $(".nav-scroll").click(function (e) {
        let targetId = $(this).data("scroll");
        $([document.documentElement, document.body]).animate({
            scrollTop: $(targetId).offset().top
        }, 1500);
    });
}

// set default tooltip to hover
$.fn.tooltip.Constructor.Default.trigger = 'hover';