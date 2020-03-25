// Check page is loading or load 
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready())
} else {
    ready()
}

function ready() {

    // Remove cart item with button
    var removeCartItemButtons = document.getElementsByClassName('btn-remove')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    // Add to cart with "Add to list Button"
    var addToCartButtons = document.getElementsByClassName('add-to-cart')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

}

// Remove Cart Item 
function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}

// Add Cart Item With add-to-cart button
function addToCartClicked(event) {
    var button = event.target
    var shopItem = button.parentElement.parentElement
    var title = shopItem.getElementsByClassName('card-title')[0].textContent;
    var price = shopItem.getElementsByClassName('card-price')[0].textContent;
    var imageSrc = shopItem.getElementsByClassName('card-img-top')[0].src;
    addItemToCart(title, price, imageSrc)
    updateCartTotal()
}

// Create cart item
function addItemToCart(title, price, imageSrc) {
    var cartRow = document.createElement('div')
    cartRow.classList.add('row')
    cartRow.classList.add('card-row')
    var cartItems = document.getElementsByClassName('cart-list')[0]
    var cartItemNames = cartItems.getElementsByClassName('product-name')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].textContent == title) {
            alert('This item is already added to the cart')
            return
        }
    }
    var cartRowContents = `
        <div class="col-sm-12 col-md-2 text-center">
        <img class="img-responsive" src="${imageSrc}" alt="prewiew" width="100" height="100" style="border-radius:5px ">
        </div>
        <div class="text-sm-center col-sm-12 text-md-center col-md-2">
        <h4 class="product-name">${title}</h4>
        <h5>
            <small>آقای مهدی شهبازی</small>
        </h5>
        </div>
        <div class="col-sm-3 col-md-4 text-md-right" style="padding-top: 5px">
            <p class = "card-price">
                <strong>${price}</strong> تومان
            </p>
        </div>
        <div class="col-sm-2 col-md-4 text-right btn-remove">
            <button type="button" class="btn btn-danger btn-remove">حذف</button>
        </div>
        <hr>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-remove')[0].addEventListener('click', removeCartItem)
}

// Update cart total price
function updateCartTotal() {
    var cartRows = document.getElementsByClassName('card-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('card-price')[0]
        var price = parseFloat(priceElement.innerText)
        total = total + price
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = total
}