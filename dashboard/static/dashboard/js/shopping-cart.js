// event handler for all new card add to button
function addToCardButtons() {
    $(".add-to-cart-button").each(function () {
        $(this).click(addToCartClicked);
    });
}


// animate to top of cart list
function animatedToCardList() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".shopping-content").offset().top
    }, 500);
}

// error modal function -> get modal id & header & message
function errorModal(modalId, modalHeader, modalMessage) {
    $(modalId).find(".modal-title").text(modalHeader);
    $(modalId).find(".modal-body-p").text(modalMessage);
    $(modalId).modal()
}

// disable and reset discount
function discountStatus(status) {
    if (status === "disable") {
        console.log("Hi")
        $("#discountCode").prop("read-only", true);
        $("#discountButton").prop("disabled", true);
    }
    // reset discount --> no required
    // else if (status === "reset") {  // reset cart items and hidden inputs
    //     errorModal("#errorModal", "خطا در اعمال کد تخفیف", "کد تخفیف شما باطل شد.");
    //     $("#totalId").val("");
    //     $("#totalPrice").val("").prop("read-only", false);
    //     $("#discountCode").val("");
    //     $("#cartListItems").empty();
    //     $(".total-price").text("0");
    //     $("#discountButton").prop("disabled", false);
    // }
}

// add cart item with add-to-cart button
function addToCartClicked() {
    let courseCard = $(this).parents(".course-card").first();
    let id = courseCard.find(".course-id").val();
    let title = courseCard.find(".title").text();
    let price = courseCard.find("#price").val();
    let teacher = courseCard.find(".teacher-name").text();
    let imageSrc = courseCard.find(".card-img-top").attr('src');
    let status = false;
    $(".cart-course-title").each(function (index, cardItemTitle) {
        if ($(cardItemTitle).text() === title) {
            errorModal("#errorModal", "مشکل در خرید دوره", "درس مورد نظر قبلا به سبد خرید اضافه شده است.");
            status = true;
        }
    });
    if (!status) addItemToCart(id, title, price, teacher, imageSrc)
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
    let cartList = $("#cartListItems");
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
    if ($(".cart-item").length === 0) {
        errorModal("#errorModal", "مشکل در خرید دوره", "سبد خرید شما خالی می باشد، یک درس را انتخاب کنید.")
        event.preventDefault();
    }
});


$('#discountButton').click(function () {
    if ($(".cart-item").length === 0) {
        errorModal("#errorModal", "مشکل در خرید دوره", "سبد خرید شما خالی می باشد، یک درس را انتخاب کنید.")
    } else {
        $.ajax({
            url: "/payment/compute-discount/",
            dataType: "json",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                code: $('#discountCode').val(),
                total_id: $('#totalId').val(),
                total_pr: $('#totalPrice').val()
            },
            beforeSend: function (xhr, settings) {
            },
            success: function (data, textStatus, xhr) {
                if (data !== 406) {
                    discountStatus("disable");
                    let oldTotalPrice = $("#totalPrice");
                    let profitPrice = parseFloat(oldTotalPrice.val()) - parseFloat(data.amount);
                    $("#profitPrice").text(profitPrice);
                    $("#discountPrice").text(data.amount);
                    // disable close modal when click outside
                    $("#discountModal").modal({backdrop: 'static', keyboard: false}).modal();
                    let discountPriceTemplate = `<span style="color: #e8505b;text-decoration: line-through">${oldTotalPrice.val()}</span> ${data.amount}`
                    oldTotalPrice.val(data.amount);
                    $(".total-price").empty().append(discountPriceTemplate)
                } else {
                    errorModal("#errorModal", "خطا در اعمال تخفیف", "کد تخفیف شما معتبر نمی باشد، دوباره امتحان کنید.")
                }

            },
            error: function (xhr, status, error) {
                alert(error);
            }
        });
    }
});


$("#modalDiscountButton").click(function () {
    $("form#shopping-cart-form").submit()
});
