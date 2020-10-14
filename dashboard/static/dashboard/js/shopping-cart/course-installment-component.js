function renderCartInstallments(course) {
    let instalmentsRowsTemplate = renderCourseInstallments(course.installments, course.id, course.discount)
    let installmentsTemplate = `
        <div id="course-${course.id}" class="container mt-3">
             <div class="row text-sm-center mb-2">
                <img src="${course.image}" width="50" height="50">
                <div class="mr-2">
                    <p class="m-0"><strong>${course.title}</strong></p>
                    <h6 class="p-0"><small>${course.teacher}</small></h6>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table text-center">
                    <thead>
                    <tr>
                        <th scope="col">شهریه</th>
                        <th scope="col">قیمت</th>
                        <th scope="col">وضعیت</th>
                        <th scope="col">
                            <button type="button" class="btn btn-primary btn-sm text-nowrap" data-id="${course.id}" onclick="selectInstallments(this)">انتخاب همه</button>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                        ${instalmentsRowsTemplate}
                    </tbody>
                </table>
            </div>
        </div>`
    $("#installments").append(installmentsTemplate)
    updateCartTotalPrice();
}


function renderCourseInstallments(instalments, courseId, disocunt) {
    let instalmentsRowsTemplate = ``
    let firstInstallment = false;
    $.each(instalments, function (index, installment) {

        instalmentsRowsTemplate += `
        <tr>
            <td scope="row">${installment.title === null ? "تمام شهریه" : installment.title}</td>
            <td>${installmentAmountRender(installment.amount, disocunt)}</td>
            <td>${installment.message}</td>
            <td class="pl-5">
                <div class="form-check">
                    <input onchange="updateCoursePrice(this)" data-course-id="${courseId}" data-amount="${installment.amount}" type="checkbox" value="${installment.id}" ${firstInstallment === false ? "disabled checked" : ""} style="width: 20px; height: 20px">
                </div>
            </td>
        </tr>`
        firstInstallment = true;
    })
    return instalmentsRowsTemplate;
}


// select all checkbox
function selectInstallments(element) {
    $("#course-" + $(element).data("id") + " input[type='checkbox']").prop('checked', true);
    updateCartTotalPrice();
}

// update total course total price
function updateCoursePrice(element) {
    let totalPrice = 0;
    $("#course-" + $(element).data("course-id") + " input:checked").each(function () {
        totalPrice += $(this).data("amount");
    })
    $("#course-cart-" + $(element).data("course-id") + " .total-amount").text(totalPrice + " تومان ")
    updateCartTotalPrice();
}

// remove course from cart
function removeCourse(element) {
    let shoppingCardIds = JSON.parse(sessionStorage.getItem("totalId"));
    let id = $(element).data("id");
    $("#course-" + id).remove();
    $("#course-cart-" + id).remove();

    // remove from local storage
    const index = shoppingCardIds.indexOf(id.toString());
    if (index > -1) {
        shoppingCardIds.splice(index, 1);
    }
    // show redirect to shopping
    if (shoppingCardIds.length === 0) noShoppingItem()
    console.log(shoppingCardIds.length)
    sessionStorage.setItem("totalId", JSON.stringify(shoppingCardIds));
    updateCartTotalPrice();
}

// update cart total credit
function updateCartTotalPrice() {
    let totalPrice = 0;
    $("#installments input:checked").each(function () {
        totalPrice += $(this).data("amount");
    })
    $("#totalPriceText").text(totalPrice)
    $("#totalPrice").val(totalPrice)
}


function installmentAmountRender(amount, discount) {
    let originalPrice = parseInt((amount * 100) / (100 - discount.percent))
    if (discount !== null) {
        return `<span class="price" style="color: #e8505b;text-decoration: line-through">${originalPrice}</span>
                <span>${amount + " تومان"}</span>`
    } else return amount + " تومان";
}
