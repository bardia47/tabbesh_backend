// event handler for all new card add to button
function addToCardButtons() {
    $(".add-to-cart-button").each(function () {
        $(this).click(addToCartClicked);
    });
}


// add cart item with add-to-cart button
function addToCartClicked() {
    let courseCard = $(this).parents(".course-card").first();
    let id = courseCard.find(".course-id").val();
    let title = courseCard.find(".title").text();
    let price = courseCard.find(".price").text();
    let teacher = courseCard.find(".teacher-name").text();
    let imageSrc = courseCard.find(".card-img-top").attr('src');
    let duplicateCourse = false;
    $(".cart-course-title").each(function (index, cardItemTitle) {
        console.log(cardItemTitle)
        console.log(title)
        if ($(cardItemTitle).text() == title) {
            $("#errorModalForCart").modal();
            $("#modal-body").text("درس مورد نظر قبلا به سبد خرید اضافه شده است.");
            duplicateCourse = true;
        }
    });
    if (!duplicateCourse) addItemToCart(id, title, price, teacher, imageSrc)
}

// create cart item
function addItemToCart(id, title, price, teacher, imageSrc) {
    let cartTemplate = `
<div class="row card-row">
    <div class="col-md-12 cart-item ">
    <div class="card">
    <div class="card-body">
      <div class="row">
        <!-- Course image -->
        <div class="col-md-1 cart-course-image">
          <img src="${imageSrc}" alt="course image">
        </div>
        <!-- Course title -->
        <div class="col-md-2 cart-course-title">
          <p class="cart-course-title">${title}</p>
        </div>
        <!--Course teacher name -->
        <div class="col-md-2 cart-course-teacher-name">
          <p>${teacher}</p>
        </div>
        <!-- Course price -->
        <div class="col-md-3 cart-price">
          <p style="font-family:'Vazir_Bold'">
          <span style="font-family:'Vazir_Light'">قیمت : </span>
          <span class="cart-price-text">${price}</span>
          </p>
      </div>
      <!-- Button-to-delete -->
        <div class="col-md-4 cart-button-to-delete">
          <button class="btn btn-danger btn-remove"><img src="/static/home/images/icons/delete.svg" alt="button link to class">حذف</button>
        </div>
      </div>
    </div>
  </div>
  <input type="hidden" class="cart-course-id" value="${id}">
  </div>
</div>`;
    let cartList = $(".cart-list");
    cartList.append(cartTemplate);
    let cartItem = cartList.children(".row").last();
    // remove cart item handler
    cartItem.find(".btn-remove").click(function () {
        $(this).parents(".card-row").remove();
        $(".shopping-title")[0].scrollIntoView();
        updateCartTotal()
    });
    animatedToCardList();
    updateCartTotal()
}

// Update cart total price
function updateCartTotal() {
    let totalPrice = 0;
    let totalId = "";
    $(".cart-item").each(function (index, cartItem) {
        let itemPrice = $(cartItem).find(".cart-price-text");
        let itemId = $(cartItem).find(".cart-course-id");
        // check if price is رایگان change to 0
        if ($(itemPrice).text() !== "رايگان!") totalPrice += parseFloat($(itemPrice).text());
        // make total id and price for back-end in hidden input
        totalId = totalId + itemId.val() + " "
    });
    totalPrice = Math.round(totalPrice * 100) / 100;
    $(".total-price").text(totalPrice);
    $("#totalPrice").val(totalPrice);
    $("#totalId").val(totalId);
}


// shopping cart button
$("#shopping-cart-form").submit(function (event) {
    console.log($("#totalId").val());
    if ($(".cart-item").length == 0) {
        $("#errorModalForCart").modal();
        $("#modal-body").text("سبد خرید شما خالی می باشد، یک درس را انتخاب کنید.");
        event.preventDefault();
    }
});


// animate to top of cart list
function animatedToCardList() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".shopping-content").offset().top
    }, 500);
}