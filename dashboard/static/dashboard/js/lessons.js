// function for get get variable in js
function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

//get lessons with ajax
$(function () {
    $.ajax({
        url: "http://127.0.0.1:8000/dashboard/test/",
        type: "GET",
        success: function (courseCards, textStatus, request) {
            renderLessenCards(courseCards)
            renderPagination(request.getResponseHeader('Last-Page'))
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
});

// hostname of project -- example : https://127.0.0.1:8000
let hostName = window.location.href.split("/")[0]

function renderLessenCards(courseCards) {
    $.each(courseCards, function (index, courseCard) {
        let endDateCourse = new persianDate(Date.parse(courseCard.end_date))
        let nextClassDate = new persianDate(Date.parse(courseCard.first_class))
        // check class is active or not
        if (courseCard.is_active) {
            buttonToClassTemplate = `
            <button class="btn btn-success mb-1">
                <img src="${hostName}/static/home/images/icons/click.svg" alt="button link to class">
                ورود به کلاس
            </button>
            `
        } else {
            buttonToClassTemplate = `
            <button class="btn btn-danger mb-1" disabled>
                <img src="${hostName}/static/home/images/icons/click.svg" alt="button link to class">
                کلاس شروع نشده
            </button>
            `
        }
        let lessonCardTemplate = `
        <!-- Course Cards -->
        <div class="col-md-4 mb-3">
            <!-- Course Card  -->
            <div class="card course-card h-100">
                <!-- Course poster -->
                <img class="card-img-top course-card-image" src="${courseCard.image}" />
                <!-- Course content -->
                <div class="card-body course-card-block">
                    <!-- Course title  -->
                    <h4 class="card-title">${courseCard.title}</h4>
                    <!-- Course teacher  -->
                    <div class="course-teacher-name">
                        <h6>استاد {{ course.teacher.get_full_name }}</h6>
                    </div>
                    <!-- Course calender for next class  -->
                    <div class="course-calender">
                        <p>
                            <img src="{% static 'home/images/icons/clock.svg' %}" alt="">
                            جلسه ی بعدی:
                            <span>
                                ${endDateCourse.format("dddd")}
                                ${endDateCourse.format("D")}
                                ام
                                ساعت
                                ${endDateCourse.format("H:m")}
                             </span>
                        </p>
                    </div>
                    <!-- End of the course  -->
                    <div class="course-end-date">
                        <p>
                            <img src="${hostName}/static/home/images/icons/calendar.svg" alt="calender-icon" />
                            اتمام دوره:
                            <span>
                                ${nextClassDate.format("dddd")}
                                ${nextClassDate.format("D")}
                                ${nextClassDate.format("MMMM")}
                            </span>
                        </p>
                    </div>
                    <!-- Description of the course  -->
                    <div class="course-description">
                        <p class="course-description-title">
                            <img src="${hostName}/static/home/images/icons/paragraph.svg" alt="" />
                            توضیحات:
                        </p>
                        <p class="course-description-p">${courseCard.description}</p>
                    </div>
                </div>
                <!-- Button link to class -->
                <div class="card-footer button-to-class p-0 py-3">
                    ${buttonToClassTemplate}
                    <button onclick="location.href='files/${courseCard.code}'" class="btn btn-dark mr-2" type="button">
                        <img src="${hostName}/static/home/images/icons/document.svg" alt="button link to class" />
                        جزوه ها
                    </button>
                </div>
            </div>
        </div>
        `
        $(".card-group").append(lessonCardTemplate)
    });
}


function renderPagination(pageNumber) {
    $('.pagination').append(`<a class="next page-numbers" href="${hostName}/"></a>"`)
    for (let i = 1; i <= pageNumber; i++) {
        $('.pagination').append(`<a class="page-numbers" href="javascript:;">${i}</a>`)
    }
    $('.pagination').append(`<a class="next page-numbers" href="javascript:;">بعدی</a>`)
}


pageNumberTemplate = `
                <a class="page-numbers" href="javascript:;">1</a>
                <a class="page-numbers" href="javascript:;">2</a>
                <span aria-current="page" class="page-numbers current">3</span>
                <a class="page-numbers" href="javascript:;">4</a>
                <a class="page-numbers" href="javascript:;">5</a>
                <a class="next page-numbers" href="javascript:;">بعدی</a>
`