$(function () {
    bestSellerAjax();
    fullDiscountAjax();

    $("#searchInput").on("keyup", function () {
        searchAjax($(this).val());
    });
});


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
                    <h4>${course.teacher_full_name}</h4>
                    <h5 class="vazir-medium">${course.lesson_title}</h5>
                    <p>${course.grade_title}</p>
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
                    <h4>${course.teacher_full_name}</h4>
                    <h5 class="vazir-medium">${course.lesson_title}</h5>
                    <p>${course.grade_title}</p>
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
                    <h4>${course.teacher_full_name}</h4>
                    <h5 class="vazir-medium">${course.lesson_title}</h5>
                    <p>${course.grade_title}</p>
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