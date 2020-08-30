$(function () {
    bestSellerAjax();

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
    })
    $("#bestSellersCourse").empty().append(coursesTemplate);
    owlCarouselInitial("#bestSellersCourse");
}

//
// function fullDiscountAjax() {
//     $.ajax({
//         url: "/best-selling-courses/",
//         type: "GET",
//         dataType: "json",
//         success: function (bestSellerCourses) {
//             bestSellerRender(bestSellerCourses)
//         },
//         error: function () {
//             alert("بارگذاری پرفروش ترین دروس به مشکل خورده است! دوباره امتحان کنید.")
//         },
//     });
// }
//
// function fullDiscountRender(bestSellerCourses) {
//     let coursesTemplate = ``;
//     $.each(bestSellerCourses, function (index, course) {
//         let courseTemplate = `
//         <div class="mx-2">
//             <div class="card">
//                 <img class="img-card" src="${course.image}" alt="course image">
//                 <div class="card-body text-center">
//                     <h4>${course.teacher_full_name}</h4>
//                     <h5 class="vazir-medium">${course.lesson_title}</h5>
//                     <p>${course.grade_title}</p>
//                 </div>
//             </div>
//         </div>
//         `;
//         coursesTemplate += courseTemplate;
//     })
//     $("#bestSellersCourse").empty().append(coursesTemplate);
//     owlCarouselInitial("#bestSellersCourse");
// }


function owlCarouselInitial(carouselId) {
    //initial changes for carousels
    $(carouselId).owlCarousel({
        rtl: true,
        loop: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            720: {
                items: 3,
                nav: true,
            }
        }
    });

    $(carouselId).find(".owl-prev").empty().append(`<img src="/static/home/images/home-page/icons/owl-prev.svg" width="40" height="40">`);
    $(carouselId).find(".owl-next").empty().append(`<img src="/static/home/images/home-page/icons/owl-next.svg" width="40" height="40">`);
}