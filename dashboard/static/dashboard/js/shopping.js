// function for get Request.GET variable
function getUrlParameter(url, param) {
    urlArray = url.split("/");
    paramets = urlArray[urlArray.length - 1];
    const urlParams = new URLSearchParams(paramets);
    return urlParams.get(param)
}

function urlMaker() {
    return getShoppingURL + searchParameter
}

function loading() {
    $(".card-group").hide();
    $(".pagination-wrapper").hide();
    $(".loading-search").show();

    setTimeout(function () {
        $(".card-group").show();
        $(".pagination-wrapper").show();
        $(".loading-search").hide();
        $(".card-group").show();
        $(".pagination-wrapper").show()
    }, 1000);
}

// hostname of project -- example : https://127.0.0.1:8000
// let arrayHref = window.location.href.split("/")
// let hostName = arrayHref[0] + "//" + arrayHref[2]
let firstParameter = new URL(window.location.href).search.slice(1);
let searchParameter;
// add to GET variable page to url parameter --> read : https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams/append
if (firstParameter) {
    searchParameter = new URLSearchParams(firstParameter)
} else {
    searchParameter = new URLSearchParams("?page=1")
}
let getShoppingURL = "/dashboard/get-shopping/?";
// first pagination when user request https://127.0.0.1:8000/dashboard/shopping/
// initial shopping page
$(function () {

    // set menu active
    $("#shoppingMenu").addClass("active-menu");

    pagination(urlMaker())
});

// pagination when user return to previous page --> hint: read about history javascript stack
window.onpopstate = function (event) {
    pagination(event.state.url)
};

//get lessons with ajax
function pagination(url) {
    // get JSON and Response Header
    $.ajax({
        url: url,
        type: "GET",
        dataType: "json",
        success: function (shoppingCards, textStatus, request) {
            $(".card-group").empty();
            $(".pagination").empty();
            renderShoppingCards(shoppingCards);
            // check if page number is not 0 show pagination
            if (shoppingCards != 0) {
                renderPagination(request.getResponseHeader('Last-Page'), url)
            } else {
                let notFoundCourseTemplate = `
                <div class="container w-100 p-1 text-center vazir-bold">
                    <div class="col-md-12 mt-3 mb-3">
                        <img class="m-auto" src="/static/dashboard/images/icons/course-not-found.svg" width="130" height="130" alt="not found course">
                    </div>
                    <div class="col-md-12">
                        <p class="text-center" style="font-size: 25px;">دوره با این ویژگی ها یافت نشد !</p>
                        <p class="text-center vazir-light" style="font-size: 20px;">با ویژگی های دیگر امتحان کنید</p>
                    </div>
                </div>
                `;
                $(".card-group").append(notFoundCourseTemplate);
            }
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
        let startDateCourse = new persianDate(Date.parse(courseCard.start_date));
        let endDateCourse = new persianDate(Date.parse(courseCard.end_date));
        let coursePriceTemplate;
        // default is price without discount
        let discountPrice = parseFloat(courseCard.amount);
        let discountTitleTemplate = ``;
        // price check -- for free courses
        if (courseCard.amount <= 0) {
            coursePriceTemplate = `رايگان!`
        } else {
            // check course price have discount or not
            if (courseCard.discount == null) {
                coursePriceTemplate = `
                ${courseCard.amount}
                <span class="currency">تومان</span>
                `
            } else {
                // add discount title if course have discount
                discountTitleTemplate = `
                <p style="text-align: center ; color: #e8505b">
                    <img src="/static/dashboard/images/icons/course-discount.svg" width="25px" height="25px">
                 با تخفیف   
                    ${courseCard.discount.title}
                </p>
                `;
                discountPrice = (parseFloat(courseCard.amount) * (100 - parseInt(courseCard.discount.percent))) / 100;
                coursePriceTemplate = `
                <span class="price" style="color: #e8505b;text-decoration: line-through">${courseCard.amount}</span>
                ${discountPrice}
                <span class="currency">تومان</span>
                `
            }
        }
        // shopping card template
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
                           <img src="/static/home/images/icons/clock.svg" alt="course clock time">
                           جلسات:
                        </p>
                     </div>
                     <!-- Start of the course  -->
                     <div class="course-start-date">
                        <p class="text-nowrap">
                           <img src="/static/home/images/icons/start-date.svg" alt="start course clock">
                           شروع دوره:
                           <span>
                           ${startDateCourse.format("dddd")}
                           ${startDateCourse.format("D")}
                           ${startDateCourse.format("MMMM")}
                           ${startDateCourse.format("YYYY")}
                           </span>
                        </p>
                     </div>
                     <!-- End of the course  -->
                     <div class="course-end-date">
                        <p class="text-nowrap">
                           <img src="/static/home/images/icons/end-date.svg" alt="end course clock">
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
                           <img src="/static/home/images/icons/paragraph.svg" alt="description">
                           توضیحات:
                        </p>
                        <div class="course-description-p pr-2">${courseCard.description}</div>
                     </div>
                     <!-- Course price -->
                     <div class="course-price">
                        ${discountTitleTemplate}
                        <p>
                           <img src="/static/home/images/icons/price.svg" alt="price">
                           قیمت:
                           <span class="price">${coursePriceTemplate}</span>
                           <input id="price" type="text" value=" ${discountPrice} تومان" hidden>
                        </p>
                     </div>
                  </div>
                  <!-- Button add course to cart -->
                  <div class="card-footer add-to-cart">
                     <button class="btn add-to-cart-button">
                     <img src="/static/home/images/icons/add-to-cart.svg"
                        alt="button link to class">
                     اضافه به سبد خرید
                     </button>
                  </div>
                  <!-- hidden lesson id for handel total buy id in shopping.js -->
                  <input type="hidden" class="course-id" value="${courseCard.id}">
               </div>
            </div>
        `;
        $(".card-group").append(shoppingCardTemplate);
        // loop for course calender times
        $.each(courseCard.course_calendars, function (index, courseCalender) {
            let courseStandardTime = new persianDate(Date.parse(courseCalender));
            let courseCalenderTemplate = `
                <p class="course-calender-time">
                    <img src="/static/home/images/icons/add-time.svg" class="animated"
                    alt="time icon">
                    ${courseStandardTime.format("dddd")} ها ساعت ${courseStandardTime.format("H:m")}
                </p>
            `
            $(".course-calender").last().append(courseCalenderTemplate)
        })

    });
    addToCardButtons();
    loading()
}

// make pagination numbers
function renderPagination(pageNumber, urlAjax) {
    page = searchParameter.get("page") ? searchParameter.get("page") : "1";
    for (let number = 1; number <= pageNumber; number++) {
        if (page == number) {
            $('.pagination').append(`<span aria-current="page" class="page-numbers current ml-3">${number}</span>`)
        } else {
            searchParameter.set("page", number.toString());
            $('.pagination').append(`<a class="page-numbers ml-3" href="?${searchParameter}">${number}</a>`)
            if (page != "1") {
                searchParameter.set("page", page)
            } else {
                searchParameter.delete("page")
            }
        }
    }
    $(".page-numbers").click(function (event) {
        event.preventDefault();
        searchParameter.set("page", getUrlParameter($(this).attr("href"), "page"))
        history.pushState({url: urlMaker()}, null, "?" + searchParameter);
        // animate to shopping card section
        pagination(urlMaker())
    });
}

// regex selector
// --> read : https://stackoverflow.com/questions/190253/jquery-selector-regular-expressions
$("select[id^='search']").change(function (event) {
    if ($(this).val() != "none") {
        searchParameter.set($(this).data("search"), $(this).val());
        searchParameter.delete("page");
    } else {
        searchParameter.delete($(this).data("search"));
    }
    history.pushState({url: urlMaker()}, null, "?" + searchParameter);
    pagination(urlMaker())
});


