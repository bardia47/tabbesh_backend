$(function () {

    teacherListAjax();
    homeCounter();
    bestSellerAjax();
    fullDiscountAjax();
    supportAjax();
    $("#searchInput").on("keyup", function () {
        searchAjax($(this).val());
    });
});


function teacherListAjax() {
    $.ajax({
        url: "/all-teacher/",
        type: "GET",
        dataType: "json",
        success: function (teachersList) {
            teacherListRender(teachersList)
        },
        error: function () {
            alert("بارگذاری دبیران به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

function homeCounter() {
    let firstTimeReach = false;
    $(window).scroll(function () {
        let hT = $('.desktop-counter').offset().top,
            hH = $('.desktop-counter').outerHeight(),
            wH = $(window).height(),
            wS = $(this).scrollTop();
        if (wS > (hT + hH - wH) && !firstTimeReach) {
            $(".counter").animationCounter({
                start: 0,
                end: 1000,
                step: 1,
                delay: 200,
            })
            firstTimeReach = true;
        }
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
                   <!-- <a href="/dashboard/shopping/?teacher=${teacher.id}" class="btn btn-secondary vazir-bold mt-2"></a> -->
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
        success: function (bestSellerCourses) {
            bestSellerRender(bestSellerCourses)
        },
        error: function () {
            alert("بارگذاری پرفروش ترین دروس به مشکل خورده است! دوباره امتحان کنید.")
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
        success: function (fullDiscountCourses) {
            fullDiscountRender(fullDiscountCourses)
        },
        error: function () {
            alert("بارگذاری پرتخفیف ترین دروس به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}

function fullDiscountRender(fullDiscountCourses) {
    let coursesTemplate = ``;
    $.each(fullDiscountCourses, function (index, course) {
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
    $("#fullDiscountCourse").empty().append(coursesTemplate);
    owlCarouselInitial("#fullDiscountCourse");
}

function searchAjax(searchText) {
    let searchLimitSize = 3;
    let request = null;
    if (searchText === $("#searchInput").val() && searchText.length >= searchLimitSize) {
        request = $.ajax({
            url: "/search-home/",
            type: "POST",
            data: {
                "title": searchText
            },
            dataType: "json",
            success: function (searchCourses) {
                searchRender(searchCourses)
            },
            error: function () {
                alert("جستجوی درس با خطا رو به رو شد! دوباره امتحان کنید.")
            },
        });
    }
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
        success: function (supports) {
            supportRender(supports)
        },
        error: function () {
            alert("بارگذاری پشتیبانی به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}
//for support
function supportRender(supports) {
    let supportsTemplate = ``;
    $.each(supports, function (index, support) {
        let supportTemplate = `
        <div class="mx-2">
            <div class="card">
                ${support.description}
            </div>
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

jQuery.event.special.touchstart = {
    setup: function (_, ns, handle) {
        if (ns.includes("noPreventDefault")) {
            this.addEventListener("touchstart", handle, {passive: false});
        } else {
            this.addEventListener("touchstart", handle, {passive: true});
        }
    }
};