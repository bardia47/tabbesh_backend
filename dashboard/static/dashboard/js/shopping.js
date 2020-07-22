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

// first pagination when user request https://127.0.0.1:8000/dashboard/shopping/
$(function () {
    url = hostName + "/dashboard/shopping/?page=" + (getUrlParameter(window.location.href, "page") ? +getUrlParameter(window.location.href, "page") : "1")

    pagination("http://127.0.0.1:8000/dashboard/get-shopping/")
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
        dataType: "json",
        success: function (shoppingCards, textStatus, request) {
            $(".card-group").empty()
            // $(".pagination").empty()
            renderShoppingCards(shoppingCards)
            // check if page number is not 0 show pagination
            // if (shoppingCards != 0) {
            //     renderPagination(request.getResponseHeader('Last-Page'), url)
            // }
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}

// Add course card to div card group
function renderShoppingCards(courseCards) {
    $.each(courseCards, function (index, courseCard) {
        // parse Date to ISO date format and use persianDate jQuery
        let startDateCourse = new persianDate(Date.parse(courseCard.start_date))
        let endDateCourse = new persianDate(Date.parse(courseCard.end_date))
        // price check -- for free courses
        if (courseCard.amount <= 0) {
            coursePriceTemplate = `رايگان!`
        } else {
            coursePriceTemplate = `
            ${courseCard.amount}
            <span class="currency">تومان</span>
            `
        }
        let shoppingCardTemplate = `
        <div class="col-md-4 mb-3">
            <div class="card course-card h-100">
                <!-- Course poster -->
                <img class="card-img-top" src="${courseCard.image}">
                <!-- Course content -->
                <div class="card-body">
                    <!-- Course title  -->
                    <h4 class="title ">${courseCard.title}</h4>
                    <!-- Course teacher name  -->
                    <div class="course-teacher-name">
                        <h6 class="teacher-name">استاد ${courseCard.teacher}</h6>
                    </div>
                    <!-- Course calender  -->
                    <div class="course-calender">
                        <p>
                            <img src="${hostName}/static/home/images/icons/clock.svg" alt="course clock time">
                            جلسات:
                        </p>
                        <!-- Loop for course calender times -->
                        {% for cc in course.course_calendar_set.all %}

                        {% endfor %}
                    </div>
                    <!-- Start of the course  -->
                    <div class="course-start-date">
                        <p>
                            <img src="${hostName}/static/home/images/icons/start-date.svg" alt="start course clock">
                            شروع دوره:
                            <span>
                                ${startDateCourse.format("dddd")}
                                ${startDateCourse.format("D")}
                                ${startDateCourse.format("MMMM")}
                            </span>
                        </p>
                    </div>
                    <!-- End of the course  -->
                    <div class="course-end-date">
                        <p>
                            <img src="${hostName}/static/home/images/icons/end-date.svg" alt="end course clock">
                            اتمام دوره:
                            <span>
                                ${endDateCourse.format("dddd")}
                                ${endDateCourse.format("D")}
                                ${endDateCourse.format("MMMM")}
                            </span>
                        </p>
                    </div>
                    <!-- Description of the course  -->
                    <div class="course-description">
                        <p class="course-description-title">
                            <img src="${hostName}/static/home/images/icons/paragraph.svg" alt="description">
                            توضیحات:
                        </p>
                        <p class="course-description-p">${courseCard.description}</p>
                    </div>
                    <!-- Course price -->
                    <div class="course-price">
                        <p>
                            <img src="${hostName}/static/home/images/icons/price.svg" alt="price">
                            قیمت:
                            <span class="price">
                            ${coursePriceTemplate}
                    </span>
                        </p>
                    </div>
                </div>
                <!-- Button add course to cart -->
                <div class="card-footer add-to-cart">
                    <button class="btn btn-success add-to-cart-button">
                        <img src="${hostName}/static/home/images/icons/add-to-cart.svg"
                             alt="button link to class">
                        اضافه به سبد خرید
                    </button>
                </div>
                <!-- hidden lesson id for handel total buy id in shopping.js -->
                <input type="hidden" class="course-id" value="{{ course.id }}">
            </div>
        </div>
        `
        $(".card-group").append(shoppingCardTemplate)
        // course calender section


    });
    $(".card-group").show()
}

// make pagination numbers
function renderPagination(pageNumber, urlAjax) {
    let url = urlAjax.substring(0, urlAjax.indexOf('?'))
    let page = (getUrlParameter(window.location.href, "page") ? getUrlParameter(window.location.href, "page") : "1")
    // $('.pagination').append(`<a class="next page-numbers" href="${hostName}/dashboard/get_lessons/"> Prev </a>`)
    console.log(pageNumber)
    for (let number = 1; number <= pageNumber; number++) {
        if (page == number) {
            $('.pagination').append(`<span aria-current="page" class="page-numbers current">${number}</span>`)
        } else {
            $('.pagination').append(`<a class="page-numbers" href="` + url + `?page=${number}">${number}</a>`)
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
