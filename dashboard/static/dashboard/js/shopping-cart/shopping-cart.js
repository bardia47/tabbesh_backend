$(function () {
    if (sessionStorage.getItem("totalId") != null) {
        loadShopping(sessionStorage.getItem("totalId"))
    } else noShoppingItem()


    window.onbeforeunload = () => {
        sessionStorage.setItem("totalId", JSON.stringify(shoppingCartsId))
    }
});

// get shopping carts
function loadShopping(courseIds) {
    // get JSON and Response Header
    $.ajax({
        url: "/payment/get-installment/",
        type: "GET",
        dataType: "json",
        data: {
            "id": courseIds
        },
        success: function (data) {
            sessionStorage.removeItem("totalId")
            renderShoppingCarts(data, true);
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}

// shopping cart payment handler
$("#payButton").click(function () {
    sessionStorage.removeItem("totalId")
    idSet();
});

// set ids of installment
function idSet() {
    let installments = [];
    $("#installments input:checked").each(function () {
        installments.push($(this).val())
    })
    $("#totalId").val(JSON.stringify(installments))
}

// discount check button handler
$('#discountButton').click(function () {
    if ($("div[id^='course-cart-']").length === 0) failedDiscountModal("دوره ای در سبد خرید موجود نمی باشد")
    else discountAjax();
});

// check discount code
function discountAjax() {
    idSet();
    $.ajax({
        url: "/payment/compute-discount/",
        dataType: "json",
        type: "GET",
        data: {
            code: $("#discountCode").val(),
            total_id: $("#totalId").val(),
            total_pr: $("#totalPrice").val()
        },
        success: function (data, status) {
            applyDiscount(data, status)
        },
        statusCode: {
            406: function (data) {
                console.log(data.responseJSON.massage)
                failedDiscountModal(data.responseJSON.message)
            }
        }
    });
}

// apply discount when status is true
function applyDiscount(data) {
    successDiscountModal(data.message)
    let oldTotalPrice = $("#totalPrice");
    let discountPriceTemplate = `<span class="text-danger" style="text-decoration: line-through">${oldTotalPrice.val()}</span> ${data.amount}`
    $("#totalPrice").val(data.amount)
    $("#discountButton").prop("disabled", true)
    $("#totalPriceText").empty().append(discountPriceTemplate)
}


// success modal for discount
function successDiscountModal(message) {
    let modalHeaderTemplate = `<h5 class="modal-title text-success"><i class="fas fa-check-circle"></i>موفق</h5>`
    let modalBodyTemplate = `
    <div class="text-center">
        <p class="vazir-bold">${message}</p>
        <p>بر روی دکمه پرداخت کلیک کنید</p>
    </div>
    `
    let modalFooterTemplate = `
    <div class="mx-auto">
        <button id="discountPayment" type="button" class="btn btn-success ml-2">پرداخت</button>
        <button id="discountRefreshButton" type="button" class="btn btn-danger">ريست تخفيف</button>    
    </div>
    `
    let template = modalRender("successDiscountModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#successDiscountModal").modal({backdrop: 'static', keyboard: false}).modal();
    $("#successDiscountModal").on("hidden.bs.modal", function () {
        $(this).remove();
    })
    // submit discount and purchase
    $("#discountPayment").click(function () {
        $("#shopping-cart-form").submit()
    });

    // reset discount
    $("#discountRefreshButton").click(function () {
        location.reload();
    });
}

// failed modal for discount
function failedDiscountModal(message) {
    let modalHeaderTemplate = `<h5 class="modal-title text-danger"><i class="fas fa-exclamation-circle ml-1"></i>خطا</h5>`
    let modalBodyTemplate = `<p class="vazir-bold text-center">${message}</p>`
    let modalFooterTemplate = `<button class="btn btn-danger w-100" data-dismiss="modal">فهمیدم!</button>`
    let template = modalRender("failedDiscountModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#failedDiscountModal").modal();
    $("#failedDiscountModal").on("hidden.bs.modal", function () {
        $(this).remove();
    })
}
