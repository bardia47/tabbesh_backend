var shoppingCardIds = [];

$(function () {

    // set menu active
    $("#shoppingMenu").addClass("active-menu");
    if (sessionStorage.getItem("totalId") != null) {
        loadShopping(sessionStorage.getItem("totalId"))
        shoppingCardIds = sessionStorage.getItem("totalId").split(',', -1);
        console.log(shoppingCardIds)
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
    e.preventDefault();
    let installments = [];
    $("#installments input:checked").each(function () {
        installments.push($(this).val())
    })
    $("#totalId").val(JSON.stringify(installments))
});


// // error modal function -> get modal id & header & message
// function errorModal(modalId, modalHeader, modalMessage) {
//     $(modalId).find(".modal-title").text(modalHeader);
//     $(modalId).find(".modal-body-p").text(modalMessage);
//     $(modalId).modal()
// }

// // disable and reset discount
// function discountStatus(status) {
//     if (status === "disable") {
//         $("#discountCode").prop("read-only", true);
//         $("#discountButton").prop("disabled", true);
//     }
//     // reset discount --> no required
//     // else if (status === "reset") {  // reset cart items and hidden inputs
//     //     errorModal("#errorModal", "خطا در اعمال کد تخفیف", "کد تخفیف شما باطل شد.");
//     //     $("#totalId").val("");
//     //     $("#totalPrice").val("").prop("read-only", false);
//     //     $("#discountCode").val("");
//     //     $("#cartListItems").empty();
//     //     $(".total-price").text("0");
//     //     $("#discountButton").prop("disabled", false);
//     // }
// }



// $('#discountButton').click(function () {
//     let discountCode = $("#discountCode");
//     discountCode.val(persianToEnglishNumbers(discountCode.val()));
//     if ($(".cart-item").length === 0) {
//         errorModal("#errorModal", "مشکل در خرید دوره", "سبد خرید شما خالی می باشد، یک درس را انتخاب کنید.")
//     } else {
//         $.ajax({
//             url: "/payment/compute-discount/",
//             dataType: "json",
//             type: "POST",
//             data: {
//                 csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
//                 code: $('#discountCode').val(),
//                 total_id: $('#totalId').val(),
//                 total_pr: $('#totalPrice').val()
//             },
//             beforeSend: function (xhr, settings) {
//             },
//             success: function (data, textStatus, xhr) {
//                 if (data !== 406) {
//                     discountStatus("disable");
//                     let oldTotalPrice = $("#totalPrice");
//                     let profitPrice = parseFloat(oldTotalPrice.val()) - parseFloat(data.amount);
//                     $("#profitPrice").text(profitPrice);
//                     $("#discountPrice").text(data.amount);
//                     // disable close modal when click outside
//                     $("#discountModal").modal({backdrop: 'static', keyboard: false}).modal();
//                     let discountPriceTemplate = `<span style="color: #e8505b;text-decoration: line-through">${oldTotalPrice.val()}</span> ${data.amount}`
//                     oldTotalPrice.val(data.amount);
//                     $(".total-price").empty().append(discountPriceTemplate)
//                 } else {
//                     errorModal("#errorModal", "خطا در اعمال تخفیف", "کد تخفیف شما معتبر نمی باشد، دوباره امتحان کنید.")
//                 }
//
//             },
//             error: function (xhr, status, error) {
//                 alert(error);
//             }
//         });
//     }
// });
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
