// Check page is loading or load 
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready())
} else {
    ready()
}

function ready() {
    // Remove cart item with button
    let removeCartItemButtons = document.getElementsByClassName('btn-remove')
    for (let i = 0; i < removeCartItemButtons.length; i++) {
        let button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    // Add to cart with "Add to list Button"
    let addToCartButtons = document.getElementsByClassName('add-to-cart-button')
    console.log(addToCartButtons)
    for (let i = 0; i < addToCartButtons.length; i++) {
        let button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

    $("#shopping-cart-form").submit(function (event) {
        let cartRows = document.getElementsByClassName('cart-item')
        if (cartRows.length === 0) {
            $("#errorModalForCart").modal();
            $("#modal-body").text("سبد خرید شما خالی می باشد، یک درس را انتخاب کنید.")
            event.preventDefault();
        } else {
            $("#shopping-cart-form").submit()
        }
    });

}

// Remove Cart Item 
function removeCartItem(event) {
    let buttonClicked = event.target
    buttoncl = buttonClicked.parentElement.parentElement.parentElement.parentElement.parentElement
    buttoncl.remove()
    updateCartTotal()
}

// Add Cart Item With add-to-cart button
function addToCartClicked(event) {
    let button = event.target
    console.log(button)
    let shopItem = button.parentElement.parentElement
    let title = shopItem.getElementsByClassName('title')[0].textContent;
    let price = shopItem.getElementsByClassName('price')[0].textContent;
    let teacher = shopItem.getElementsByClassName('teacher-name')[0].textContent;
    let imageSrc = shopItem.getElementsByClassName('card-img-top')[0].src;
    let id = shopItem.getElementsByClassName('course-id')[0].value;
    addItemToCart(title, price, teacher, imageSrc, id)
    updateCartTotal()
}

// Create cart item
function addItemToCart(title, price, teacher, imageSrc, id) {
    console.log("HI")
    let cartRow = document.createElement('div')
    cartRow.classList.add('row')
    cartRow.classList.add('card-row')
    let cartItems = document.getElementsByClassName('cart-list')[0]
    let cartItemNames = cartItems.getElementsByClassName('cart-course-title')
    for (let i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].textContent == title) {
            $("#errorModalForCart").modal();
            $("#modal-body").text("درس مورد نظر قبلا به سبد خرید اضافه شده است.")
            return
        }
    }
    let cartRowContents = `
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
  </div>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-remove')[0].addEventListener('click', removeCartItem)
    cartItems.parentElement.scrollIntoView();
}

// Update cart total price
function updateCartTotal() {
    let cartRows = document.getElementsByClassName('cart-item')
    let total = 0
    let total_id = ""
    for (let i = 0; i < cartRows.length; i++) {
        let cartRow = cartRows[i]
        let priceElement = cartRow.getElementsByClassName('cart-price-text')[0]
        console.log(priceElement)
        if (priceElement.innerText == "رايگان!") {
            price = 0;
        } else {
            price = parseFloat(priceElement.innerText)
        }
        let id = cartRow.getElementsByClassName('cart-course-id')[0].value
        total = total + price
        total_id = total_id + id + " "
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('total-price')[0].innerText = total.toLocaleString()
    // send total id to input
    document.getElementById('total_id').value = total_id
    document.getElementById('total_pr').value = total
}