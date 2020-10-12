// create cart item
function renderCartItems(installmentCards) {
    let cartTemplate, cartList = $("#cartListItems");

    $.each(installmentCards, function (index, course) {
        cartTemplate = `
            <div id="course-cart-${course.id}" class="card">
            <div class="card-body">
              <div class="row text-center">
                <!-- Course image -->
                <div class="col-md-2">
                  <img class="rounded" src="${course.image}" alt="course image" width="60px">
                </div>
                <!-- Course title -->
                <div class="col-md-3">
                  <p>${course.title}</p>
                </div>
                <!--Course teacher name -->
                <div class="col-md-3">
                  <p>${course.teacher}</p>
                </div>
                <!-- Button-to-delete -->
                <div class="col-md-4">
                  <button class="btn btn-danger" data-id="${course.id}" onclick="removeCourse(this)">
                  حذف
                  <img src="/static/home/images/icons/delete.svg" alt="button link to class" width="20px">
                  </button>
                </div>
              </div>
            </div>
          </div>`;

        cartList.append(cartTemplate);

        // render course installment
        let instalmentsRowsTemplate = renderCourseInstallments(course.installments)

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
    })

}


function renderCourseInstallments(instalments) {
    let instalmentsRowsTemplate = ``
    let firstInstallment = false;
    $.each(instalments, function (index, installment) {

        instalmentsRowsTemplate += `
        <tr>
            <td scope="row">${installment.title === null ? "تمام شهریه" : installment.title}</td>
            <td>${installment.amount + " تومان"}</td>
            <td></td>
            <td class="pl-5">
                <div class="form-check">
                    <input onchange="updateCartTotalPrice(this)" data-amount="${installment.amount}" type="checkbox" value="${installment.id}" ${firstInstallment === false ? "disabled checked" : ""} style="width: 20px; height: 20px">
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
    if (shoppingCardIds.length === 1) noShoppingItem()
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


function noShoppingItem() {
    let template = `
    <!-- no cart list item -->
    <div class="d-flex justify-content-center text-center flex- flex-column shadow-sm bg-white p-2">
        <img class="m-auto" src="/static/home/images/icons/sad-emoji.svg" width="80" height="80">
        <p class="vazir-bold">سبد خرید شما خالی می باشد!</p>
        <p class="mt-n3 text-center vazir-light">
            برای مشاهده و خرید درس بر روی دکمه ی زیر کلیک کنید
        </p>
        <a class="btn btn-dark mx-auto btn-sm" href="/dashboard/shopping/">برگشت به خرید درس</a>
    </div>
    `

    $("#cartListItems").append(template)
}