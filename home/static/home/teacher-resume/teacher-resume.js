$(function () {
    getTeacherResume();
})


function getTeacherResume() {
    $.ajax({
        url: "",
        type: "GET",
        dataType: "json",
        success: function (data) {
            document.title = data.get_full_name
            renderTeacherResume(data)
            renderTeacherCourse(data);
        },
        error: function () {
            console.log("بارگذاری رزومه دبیران به مشکل خورده است! دوباره امتحان کنید.")
        },
    });
}


function renderTeacherResume(teacherResume) {
    const teacherResumeTemplate = `
        <div class="row justify-content-center align-items-center background">
            <img src="/static/home/images/teacher-resume/resume.svg" width="30">
            <h1 class="vazir-bold h2 mr-2">${"رزومه استاد " + teacherResume.get_full_name}</h1>
        </div>
        <div class="container mt-2">
            <div class="row align-items-center px-2">
                <img class="rounded-circle" src="${teacherResume.avatar}" width="120" height="120">
                <div class="mr-2">
                    <p class="vazir-bold m-0">${"استاد " + teacherResume.get_full_name}</p>
                    <p class="m-0">${teacherResume.grade_choice}</p>
                </div>
            </div>
            <hr class="w-100 bg-secondary" style="height: 2px">
            <div class="px-5">
                ${teacherResume.description === null ? "رزومه‌ای برای مشاهده موجود نیست " : teacherResume.description}
            </div>
        </div>
    `
    $("#teacherResume").append(teacherResumeTemplate);
}


function renderTeacherCourse(teacherCourses) {

    const teacherCoursesTemplate = `
        <div class="row justify-content-center align-items-center background">
            <img src="/static/home/images/teacher-resume/study.svg" width="40">
            <h1 class="vazir-bold h2 mr-2">${"دوره‌های استاد " + teacherCourses.get_full_name}</h1>
        </div>
        <div class="container mt-5">
            <div class="row px-2">
                ${renderCourseCards(teacherCourses.courses, teacherCourses.url)}
            </div>
        </div>
    `
    $("#teacherCourses").append(teacherCoursesTemplate);
    $(".countdown").each(function () {
        try {
            const countDown = $(this)
            $(this).countdown(countDown.data("date").replace("T", " "), (event) => $(this).text(event.strftime('%D:%H:%M:%S')))
                .on('finish.countdown', (event) => $(this).text(event.strftime('مهلت تخفیف به پایان رسید')))
        } catch (e) {
            console.log(e)
        }
    });
}


function renderCourseCards(courses, url) {
    let courseTemplate = ``;
    $.each(courses, function (index, course) {
        courseTemplate += `
            <div class="col-md-3">
                <div class="card">
                    <img class="img-card" src="${course.image}" alt="course image">
                    <div class="card-body text-center">
                        <p class="vazir-bold mb-0">${course.title}</p>
                        <!--<p class="vazir-medium mb-1">${"پایه " + course.grade}</p>-->
                        ${renderCoursePrice(course.discount, course.amount)}
                        <a href="${url}" class="btn btn-secondary vazir-bold mt-2">خرید دوره</a>
                    </div>
                </div>
            </div>
        `;
    });
    return courseTemplate;
}

function renderCoursePrice(discount, amount) {
    let amountTemplate = ``;
    if (discount === null) {
        amountTemplate = `<p> <span class="vazir-bold">قیمت:</span> ${amount + " تومان "}</p>`;
    } else {
        amountTemplate += `<p class="vazir-medium text-center text-primary mb-1">
                           <img src="/static/home/images/home-page/icons/offer.svg" width="25px" height="25px">
             با تخفیف               ${discount.title}</p>`;
        let originalPrice = parseInt((amount * 100) / (100 - discount.percent))
        amountTemplate += `<p class="mb-1"><span class="vazir-bold">قیمت:</span>
                           <span style="color: #e8505b;text-decoration: line-through">${originalPrice}</span>
                            ${amount + " تومان "}
                           </p>
                           `
        if (discount.end_date !== null) {
            amountTemplate += `
            <div class="d-flex justify-content-center text-black-50 timer vazir-bold" dir="ltr">
                <div class="mr-1"><i class="fas fa-clock"></i></div>
                <div class="countdown" data-date="${discount.end_date}" ></div>
            </div>`
        }
    }
    return amountTemplate;
}
