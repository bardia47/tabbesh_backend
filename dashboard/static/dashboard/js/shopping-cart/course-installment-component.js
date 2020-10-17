function renderCartInstallments(course) {
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
                        ${renderCourseInstallments(course.installments, course.id, course.discount)}
                    </tbody>
                </table>
            </div>
        </div>`
    $("#installments").append(installmentsTemplate)
    updateCoursePrice()
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
            <td>${installmentCheckBox(courseId, installment, firstInstallment)}</td>
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

// update course total price
function updateCoursePrice(courseId) {
    let totalPrice = 0;
    $("#course-" + courseId + " input:checked").each(function () {
        totalPrice += $(this).data("amount");
    })
    $("#course-cart-" + courseId + " .total-amount").text(totalPrice + " تومان ")
    updateCartTotalPrice();
}

// remove course from cart
function removeCourse(element) {
    let id = $(element).data("id");
    $("#course-" + id).remove();
    $("#course-cart-" + id).remove();
    removeArray(shoppingCartsId , id.toString())
    if ($("#installments input:checked").length === 0) noShoppingItem()
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
    if (discount !== null) {
        let originalPrice = parseInt((amount * 100) / (100 - discount.percent))
        return `<span class="price" style="color: #e8505b;text-decoration: line-through">${originalPrice}</span>
                <span>${amount + " تومان"}</span>`
    } else return amount + " تومان";
}


function installmentCheckBox(courseId, installment) {
    if (!installment.is_bought) {
        return `<div class="form-check">
                    <input onchange="updateCoursePrice($(this).data('course-id').toString())" data-course-id="${courseId}" data-amount="${installment.amount}" type="checkbox" value="${installment.id}" checked style="width: 20px; height: 20px">
                </div>`
    } else return ``
}