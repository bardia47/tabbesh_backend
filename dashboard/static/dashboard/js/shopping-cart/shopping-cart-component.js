const shoppingCartsId = [];
function renderShoppingCarts(carts, installmentStatus) {
    if (carts.length === 0 && installmentStatus) noShoppingItem()
    let cartTemplate = ``;
    let amountTemplate = ``
    $.each(carts, function (index, cart) {
        shoppingCartsId.push(cart.id.toString())
        cartTemplate = `
            <div id="course-cart-${cart.id}" class="card">
            <div class="card-body">
              <div class="row text-center">
                <!-- Course image -->
                <div class="col-md-1">
                  <img class="rounded" src="${cart.image}" alt="course image" width="60px">
                </div>
                <!-- Course title -->
                <div class="col-md-2">
                  <p>${cart.title}</p>
                </div>
                <!--Course teacher name -->
                <div class="col-md-2">
                  <p>${cart.teacher}</p>
                </div>
                <!-- course price -->
                <div class="col-md-3">
                <p class="text-nowrap">
                <span>پرداختی:</span>
                    ${amountRender(cart.installments, cart.discount)}
                </p>
                </div>
                <!-- Button-to-delete -->
                <div class="col-md-4">
                  <button class="btn btn-danger" data-id="${cart.id}" onclick="removeCourse(this)">
                  حذف
                  <img src="/static/home/images/icons/delete.svg" alt="button link to class" width="20px">
                  </button>
                </div>
              </div>
            </div>
          </div>`;

        $("#cartListItems").append(cartTemplate);
        if (installmentStatus === true) renderCartInstallments(cart)
    })
}


// no shopping item handler
function noShoppingItem() {
    let template = `
    <!-- no cart list item -->
    <div class="d-flex justify-content-center text-center flex- flex-column shadow-sm bg-white p-2">
        <img class="m-auto" src="/static/home/images/icons/sad-emoji.svg" width="80" height="80">
        <p class="vazir-bold">سبد خرید شما خالی می باشد!</p>
        <p class="mt-n3 text-center vazir-light">
            برای بازگشت به صفحه ی قبلی بر روی دکمه ی زیر کلیک کنید
        </p>
        <a class="btn btn-dark mx-auto btn-sm" href="javascript:history.back()">برگشت به صفحه ی قبل</a>
    </div>
    `

    $("#cartListItems").append(template)
}


function amountRender(installments, discount) {
    let amount = 0
    $.each(installments, function (index, installment) {
        amount += installment.amount;
    })
    if (discount !== null) {
        let discountMessage = ` با ${discount.percent} درصد تخفیف`;
        return `<strong class="text-success mx-1">${discountMessage}</strong>
                <span class="total-amount">${amount + " تومان"}</span>
                `
    } else return `<span class="total-amount">${amount + " تومان"}</span>`;
}


function removeArray(array, value) {
    const index = array.indexOf(value);
    if (index > -1) {
        array.splice(index, 1);
    }
}
