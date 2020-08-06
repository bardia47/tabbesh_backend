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
let getShoppingURL =  "/dashboard/get-shopping/?";
// first pagination when user request https://127.0.0.1:8000/dashboard/shopping/
$(function () {
    pagination(urlMaker())
});

// pagination when user return to previous page --> hint: read about history javascript stack
window.onpopstate = function (event) {
    console.log(event.state.url);
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
                           <img src="/static/home/images/icons/clock.svg" alt="course clock time">
                           جلسات:
                        </p>
                     </div>
                     <!-- Start of the course  -->
                     <div class="course-start-date">
                        <p>
                           <img src="/static/home/images/icons/start-date.svg" alt="start course clock">
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
                           <img src="/static/home/images/icons/end-date.svg" alt="end course clock">
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
                           <img src="/static/home/images/icons/paragraph.svg" alt="description">
                           توضیحات:
                        </p>
                        <p class="course-description-p">${courseCard.description}</p>
                     </div>
                     <!-- Course price -->
                     <div class="course-price">
                        <p>
                           <img src="/static/home/images/icons/price.svg" alt="price">
                           قیمت:
                           <span class="price">${coursePriceTemplate}</span>
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
        console.log($(this).data("search"))
        searchParameter.delete($(this).data("search"));
    }
    history.pushState({url: urlMaker()}, null, "?" + searchParameter);
    pagination(urlMaker())
});


$('#discountButton').click(function() {
	$.ajax({
		url : "/payment/compute-discount/",
		dataType : "json",
         type: "post",
		data : {
			code : $('#discountCode').attr("value"),
            total_id : $('#totalId').attr("value"),
		    total_pr : $('#totalPrice').attr("value")

        },
		beforeSend : function(xhr, settings) {
			  $('#discountButton').prop("disabled",true);
			  $('#payButton').prop("disabled",true);
			  $('#discountCode').prop("readOnly",true);
		},
		success : function(data) {
		    	  alert("کد تخفیف اعمال گردید!  ")
                  $('#totalPrice').value=data['amount']

		},
		statusCode: {
		      406: function( data ) {
		          $('#discountButton').prop("disabled",false);
		    	  alert("کد تخفیف معتبر نمیباشد")
		      }
		    },
        error:function()
        {
           alert("خطا در اتصال به سامانه")
        },
		complete:function()
		{
			$('#payButton').prop("disabled",false);
		}
	});
});