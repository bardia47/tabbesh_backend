var shoppingCardIds = [];

$(function () {
    // set menu active
    $("#shoppingMenu").addClass("active-menu");
    if (sessionStorage.getItem("totalId") != null) {
        loadShopping(sessionStorage.getItem("totalId"))
        shoppingCardIds = sessionStorage.getItem("totalId").split(',', -1);
    }
});


//get lessons with ajax
function loadShopping(ids) {
    console.log(ids)
    // get JSON and Response Header
    $.ajax({
        url: "/payment/get-installment/",
        type: "GET",
        dataType: "json",
        data: {
            "id": ids
        },
        success: function (installmentCards, textStatus, request) {
            console.log(installmentCards);
            renderCartItems(installmentCards);
            localStorage.removeItem("totalId")
        },
        error: function () {
            alert("خطا در بارگزاری دروس ... لطفا دوباره امتحان کنید!")
        },
    });
}




$("#payButton").click(function (e) {
    idSet();
});


function idSet() {
    let installments = [];
    $("#installments input:checked").each(function () {
        installments.push($(this).val())
    })
    $("#totalId").val(JSON.stringify(installments))
}




$('#discountButton').click(function () {
    if ($("div[id^='course-cart-']").length === 0) failedDiscountModal("خطا در تخفیف")
    else discountAjax();
});


function discountAjax() {
    idSet();
    $.ajax({
        url: "/payment/compute-discount/",
        dataType: "json",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            code: $("#discountCode").val(),
            total_id: $("#totalId").val(),
            total_pr: $("#totalPrice").val()
        },
        success: function (data) {
            discountStatus(data)
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText)
            alert(xhr);
        }
    });
}


function discountStatus(data) {
    if (data === 406) failedDiscountModal("کد تخفیف مشکل داره")
    else {
        successDiscountModal(data.massage)
        let oldTotalPrice = $("#totalPrice");
        let discountPriceTemplate = `<span class="text-danger" style="text-decoration: line-through">${oldTotalPrice.val()}</span> ${data.amount}`
        $("#totalPrice").val(data.amount)
        $("#discountButton").prop("disabled", true)
        $("#totalPriceText").empty().append(discountPriceTemplate)
    }
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
    let modalFooterTemplate = ``
    let template = modalRender("successDiscountModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#successDiscountModal").modal();
}

// failed modal for discount
function failedDiscountModal(message) {
    let modalHeaderTemplate = `<h5 class="modal-title text-danger"><i class="fas fa-exclamation-circle ml-1"></i>خطا</h5>`
    let modalBodyTemplate = ``
    let modalFooterTemplate = `<button class="btn btn-danger w-100" data-dismiss="modal">فهمیدم!</button>`
    let template = modalRender("failedDiscountModal", modalHeaderTemplate, modalBodyTemplate, modalFooterTemplate)
    $("body").append(template);
    $("#failedDiscountModal").modal();
}


//
//
// $("#modalDiscountButton").click(function () {
//     $("form#shopping-cart-form").submit()
// });
//
// // reset discount
// $("#discountRefreshButton").click(function () {
//     location.reload();
// });