// function for get Request.GET variable
function getUrlParameter(url, param) {
    urlArray = url.split("/");
    paramets = urlArray[urlArray.length - 1];
    const urlParams = new URLSearchParams(paramets);
    return urlParams.get(param)
}

// initial page javascript
$(function () {

    // set menu active
    $("#lessonsMenu").addClass("active-menu");

    url = "/dashboard/get-lessons/?page=" + (getUrlParameter(window.location.href, "page") ? +getUrlParameter(window.location.href, "page") : "1")
    pagination(url)
});

// pagination when user return to previous page --> hint: read about history javascript stack
window.onpopstate = function (event) {
    pagination(event.state.url)
};

//get lessons with ajax
function pagination(url) {
    // check with page go


    // get JSON and Response Header
    $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        success: function (courseCards, textStatus, request) {
            $("#activeCourses").empty();
            $("#finishedCourses").empty();
            $(".pagination").empty();
            renderLessenCards(courseCards);
            if (courseCards !== 0) {
                renderPagination(request.getResponseHeader('Last-Page'), url)
            }
        },
        error: function () {
            var element = $("#have-class");
            if (!element.length || element.val() !== "False")
                alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}

// Add course card to div card group
function renderLessenCards(courseCards) {
    $.each(courseCards, function (index, courseCard) {
        // parse Date to ISO date format and use persianDate jQuery
        let endDateCourse = new persianDate(Date.parse(courseCard.end_date));
        let nextClassDate = new persianDate(Date.parse(courseCard.first_class));
        let nowDate = new persianDate();
        let grayImg = "";
        let classActive = endDateCourse >= nowDate;
        let buttonToClassTemplate = ``;
        let buttonToClassPanel = ``;
        let nextClassTemplate = ``;

        // if user is student --> show file manager otherwise show teacher panel
        if ($("#roleStatus").val() === "False") {
            buttonToClassPanel = `
            <button onclick="location.href='teacher_course_panel/${courseCard.code}'" class="btn btn-dark mr-2" type="button">
                <img src="/static/home/images/icons/teacher-panel.svg" alt="teacher panel" />
                پنل کلاس
            </button>
            `
        } else {
            buttonToClassPanel = `
            <button onclick="location.href='student_course_panel/${courseCard.code}'" class="btn btn-dark mr-2" type="button">
                <img src="/static/home/images/icons/teacher-panel.svg" alt="student panel" />
                پنل کلاس
            </button>
            `
        }
        if (classActive) {
            nextClassTemplate = `
                <p>
                    <img class="${grayImg}" src="/static/home/images/icons/clock.svg" alt="course calender">
                    جلسه ی بعدی:
                    <span>
                    
                        ${nextClassDate.format("dddd")}
                        ${nextClassDate.format("D")}
                        ام
                        ساعت
                        ${nextClassDate.format("H:m")}
                     </span>
                </p>
                `;
            if (courseCard.is_active) {
                buttonToClassTemplate = `
                <a class="btn btn-success mb-1" href="${courseCard.url}" target="_blank">
                    <img src="/static/home/images/icons/click.svg" alt="button link to class">
                    ورود به کلاس
                </a>
                `;
            } else {
                buttonToClassTemplate = `
                <button class="btn btn-danger mb-1" disabled>
                    <img src="/static/home/images/icons/click.svg" alt="disable button to class">
                    کلاس شروع نشده
                </button>
                `;
            }
        } else {
            grayImg = "gray-img";
        }
        // check first class is null
        if (courseCard.first_class == null) {
            nextClassTemplate = ``;
        }
        let lessonCardTemplate = `
            <!-- Course Cards -->
            <div class="col-md-4 mb-3 ${grayImg}">
                <!-- Course Card  -->
                <div class="card course-card h-100">
                    <!-- Course poster -->
                    <img class="card-img-top course-card-image" src="${courseCard.image}" alt="course poster" />
                    <!-- Course content -->
                    <div class="card-body course-card-block">
                        <!-- Course title  -->
                        <h4 class="card-title">${courseCard.title}</h4>
                        <!-- Course teacher  -->
                        <div class="course-teacher-name">
                            <h6>استاد ${courseCard.teacher}</h6>
                        </div>
                        <!-- Course calender for next class  -->
                        <div class="course-calender">
                            ${nextClassTemplate}
                        </div>
                        <!-- End of the course  -->
                        <div class="course-end-date">
                            <p class="text-nowrap">
                                <img src="/static/home/images/icons/calendar.svg" alt="calender-icon" />
                                اتمام دوره:
                                <span>
                                    ${endDateCourse.format("dddd")}
                                    ${endDateCourse.format("D")}
                                    ${endDateCourse.format("MMMM")}
                                    ${endDateCourse.format("YYYY")}
                                </span>
                            </p>
                        </div>
                        <!-- Description of the course  -->
                        <div class="course-description">
                            <p class="course-description-title">
                                <img src="/static/home/images/icons/paragraph.svg" alt="" />
                                توضیحات:
                            </p>
                            <div class="course-description-p pr-2">${courseCard.private_description}</div>
                        </div>
                    </div>
                    <!-- Button link to class -->
                    <div class="card-footer button-to-class p-0 py-3">
                        ${buttonToClassTemplate}
                        ${buttonToClassPanel}
                    </div>
                </div>
            </div>
        `;
        if (classActive) $("#activeCourses").append(lessonCardTemplate);
        else $("#finishedCourses").append(lessonCardTemplate)

    });
    $(".card-group").show()
}

// make pagination numbers
function renderPagination(pageNumber, urlAjax) {
    url = urlAjax.substring(0, urlAjax.indexOf('?'));
    page = (getUrlParameter(window.location.href, "page") ? getUrlParameter(window.location.href, "page") : "1");
    // $('.pagination').append(`<a class="next page-numbers" href="${hostName}/dashboard/get_lessons/"> Prev </a>`)
    for (let number = 1; number <= pageNumber; number++) {
        if (page == number) {
            $('.pagination').append(`<span aria-current="page" class="page-numbers current ml-3">${number}</span>`)
        } else {
            $('.pagination').append(`<a class="page-numbers ml-3" href="` + url + `?page=${number}">${number}</a>`)
        }
    }
    $(".page-numbers").click(function (event) {
        event.preventDefault();
        history.pushState({url: $(this).attr("href")}, null, "?page=" + getUrlParameter($(this).attr("href"), "page"));
        pagination($(this).attr("href"))
    });
    // $('.pagination').append(`<a class="next page-numbers" href="${hostName}"> Next </a>`)
    $(".pagination-wrapper").show();
    $("html, body").animate({scrollTop: 0}, "slow");
}