// function for get Request.GET variable
function getUrlParameter(url, param) {
    urlArray = url.split("/")
    paramets = urlArray[urlArray.length - 1]
    const urlParams = new URLSearchParams(paramets);
    return urlParams.get(param)
}

// hostname of project -- example : https://127.0.0.1:8000
let arrayHref = window.location.href.split("/")
let hostName = arrayHref[0] + "//" + arrayHref[2]

// first pagination when user request https://127.0.0.1:8000/dashboard/lessons/
$(function () {
    url = hostName + "/dashboard/get-lessons/?page=" + (getUrlParameter(window.location.href, "page") ? +getUrlParameter(window.location.href, "page") : "1")

    pagination(url)
})

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
        success: function (courseCards, textStatus, request) {
            $(".card-group").empty()
            $(".pagination").empty()
            renderLessenCards(courseCards)
            if (courseCards != 0) {
                renderPagination(request.getResponseHeader('Last-Page'), url)
            }
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}

// Add course card to div card group
function renderLessenCards(courseCards) {
    $.each(courseCards, function (index, courseCard) {
        // parse Date to ISO date format and use persianDate jQuery
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
                        <h6>استاد ${courseCard.teacher}</h6>
                    </div>
                    <!-- Course calender for next class  -->
                    <div class="course-calender">
                        <p>
                            <img src="${hostName}/static/home/images/icons/clock.svg" alt="">
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
    $(".card-group").show()
}

// make pagination numbers
function renderPagination(pageNumber, urlAjax) {
    url = urlAjax.substring(0, urlAjax.indexOf('?'))
    page = (getUrlParameter(window.location.href, "page") ? getUrlParameter(window.location.href, "page") : "1")
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
    $(".pagination-wrapper").show()
    $("html, body").animate({scrollTop: 0}, "slow");
}