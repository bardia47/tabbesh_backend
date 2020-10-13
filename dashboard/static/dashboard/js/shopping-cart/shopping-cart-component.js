function renderShoppingCarts(carts, installmentStatus) {
    let totalId = []; // for add buy lesson ids
    if (carts.length === 0 && installmentStatus) noShoppingItem()
    let cartTemplate = ``;
    $.each(carts, function (index, cart) {
        totalId.push(cart.id.toString())
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
                  <p><b class="ml-2">پرداختی:</b><span class="total-amount">${cart.installments[0].amount + " تومان"}</span></p>
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
    sessionStorage.setItem("totalId", JSON.stringify(totalId));
}


// no shopping item handler
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