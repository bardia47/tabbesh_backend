let firstParameter = new URL(window.location.href).search.slice(1);
let searchParameter;

if (firstParameter) {
    searchParameter = new URLSearchParams(firstParameter)
} else {
    searchParameter = new URLSearchParams("?page=1")
}

let getShoppingURL = "/dashboard/shopping-courses/?";
// first pagination when user request https://127.0.0.1:8000/dashboard/shopping/
// initial shopping page
$(function () {
    // load shopping cart
    if (sessionStorage.getItem("totalId") !== null) {
        getShoppingCart(JSON.stringify(shoppingCartsId))
    }


    // set menu active
    $("#shoppingMenu").addClass("active-menu");

    pagination(urlMaker())
});


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
        try {
            // parse Date to ISO date format and use persianDate jQuery
            let startDateCourse = new persianDate(Date.parse(courseCard.start_date));
            let endDateCourse = new persianDate(Date.parse(courseCard.end_date));
            let coursePriceTemplate;
            // default is price without discount
            let discountPrice = parseFloat(courseCard.amount);
            let discountTitleTemplate = ``, discountTimerTemplate = ``;
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
                    </p>`;
                    if (courseCard.discount.end_date !== null) {
                        discountTimerTemplate = `
                        <div class="d-flex justify-content-center text-black-50 timer vazir-bold" dir="ltr">
                            <div class="mr-1"><i class="fas fa-clock"></i></div>
                            <div class="countdown" data-date="${courseCard.discount.end_date}" ></div>
                        </div>`
                    }

                    let originalPrice = parseInt((courseCard.amount * 100) / (100 - courseCard.discount.percent))
                    coursePriceTemplate = `
                    <span class="price" style="color: #e8505b;text-decoration: line-through">${originalPrice}</span>
                    ${courseCard.amount}
                    <span class="currency">تومان</span>`
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
                           <input class="priceId" type="text" value=" ${discountPrice} تومان" hidden>
                        </p>
                     </div>
                     <!-- dicount timer -->
                     ${discountTimerTemplate}
                  </div>
                  <!-- Button add course to cart -->
                  <div class="card-footer add-to-cart">
                     <button data-course-id="${courseCard.id}" class="btn add-to-cart-button" onclick="addToCartHandler(this)">
                     <img src="/static/home/images/icons/add-to-cart.svg"
                        alt="button link to class">
                     اضافه به سبد خرید
                     </button>
                  </div>
                  <!-- course id  -->
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
        } catch (error) {
            console.log("failed to add shopping card", error);
        }


    });
    $(".countdown").each(function () {
        try {
            const countDown = $(this)
            $(this).countdown(countDown.data("date").replace("T", " "), (event) => $(this).text(event.strftime('%D:%H:%M:%S')))
                .on('finish.countdown', (event) => $(this).text(event.strftime('مهلت تخفیف به پایان رسید')))
        } catch (e) {
            console.log(e)
        }
    });
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


// event handler for all new card add to button
function addToCartHandler(event) {
    const courseId = $(event).data("course-id").toString();
    if (shoppingCartsId.indexOf(courseId) !== -1) duplicateCartItemModal()
    else {
        shoppingCartsId.push(courseId);
        sessionStorage.setItem("totalId", JSON.stringify(shoppingCartsId))
        getShoppingCart(`[${courseId}]`)
    }
}

// get shopping cart information
function getShoppingCart(courseId) {
    $.get(`/payment/installments/?id=${courseId}`, function (data) {
        renderShoppingCarts(data, false);
        animatedToCardList();
    });
}


function duplicateCartItemModal() {
    let modalHeaderTemplate = `<h5 class="modal-title text-danger"><i class="fas fa-exclamation-circle ml-1"></i>خطا در خرید دوره</h5>`
    let modalBodyTemplate = `<p class="vazir-bold text-center">درس مورد نظر قبلا به سبد خرید اضافه شده است</p>`
    let modalFooterTemplate = `<button class="btn btn-danger w-100" data-dismiss="modal">فهمیدم!</button>`
    let template = modalRender("duplicateFailedModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#duplicateFailedModal").modal();
    $("#duplicateFailedModal").on("hidden.bs.modal", function (e) {
        $(this).remove();
    })
}

function emptyShoppingCart() {
    let modalHeaderTemplate = `<h5 class="modal-title text-danger"><i class="fas fa-exclamation-circle ml-1"></i>خطا در خرید دوره</h5>`
    let modalBodyTemplate = `<p class="vazir-bold text-center">سبد خرید خالی می باشد</p>`
    let modalFooterTemplate = `<button class="btn btn-danger w-100" data-dismiss="modal">فهمیدم!</button>`
    let template = modalRender("emptyShoppingCartModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#emptyShoppingCartModal").modal();
    $("#emptyShoppingCartModal").on("hidden.bs.modal", function (e) {
        $(this).remove();
    })
}

// animate to top of cart list
function animatedToCardList() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".shopping-content").offset().top
    }, 500);
}

// remove course function
function removeCourse(event) {
    let id = $(event).data("id");
    $("#course-cart-" + id).remove();

    // remove id from courseCardsId list
    removeArray(shoppingCartsId, id.toString())
}

$("#completeShoppingBtn").click(function (e) {
    if (shoppingCartsId.length !== 0) sessionStorage.setItem("totalId", JSON.stringify(shoppingCartsId))
    else {
        e.preventDefault();
        emptyShoppingCart()
    }
});