// Frontend JS by Himanshu Choudhary
// Team TechTribe - Pemiya Rishikesh Institute of Technology

// ===== UTILITY FUNCTION =====
function escapeHtml(text) {
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// ===== CART MANAGEMENT =====

/**
 * Update cart count badge on navbar
 */
function updateCartCount() {
    fetch('/api/cart')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var items = data.items || [];
            var count = items.length;
            var badge = document.getElementById('cart-count');
            if (badge) {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'inline-block' : 'none';
            }
        }
    })
    .catch(error => console.error("Error updating cart count:", error));
}

/**
 * Add product to cart (with server-side session storage)
 */
function addToCartQuick(productId, productName, price) {
    fetch('/api/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            product_id: productId, 
            name: productName, 
            price: price,
            quantity: 1 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✓ "${productName}" added to cart!`);
            updateCartCount();
        } else {
            alert("Error adding to cart: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Connection error. Please try again.");
    });
}

/**
 * Remove item from cart
 */
function removeFromCart(productId) {
    fetch('/api/cart', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Item removed from cart");
            location.reload(); // Refresh cart page
        } else {
            alert("Error removing item");
        }
    })
    .catch(error => console.error("Error:", error));
}

/**
 * Load order summary (for checkout page)
 */
function loadOrderSummary() {
    fetch('/api/cart')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var items = data.items || [];
            var subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            var shipping = 50;
            var total = subtotal + shipping;

            // Update summary elements if they exist
            var subtotalEl = document.getElementById('order-subtotal');
            var shippingEl = document.getElementById('order-shipping');
            var totalEl = document.getElementById('order-total');

            if (subtotalEl) subtotalEl.textContent = '₹' + subtotal.toFixed(2);
            if (shippingEl) shippingEl.textContent = '₹' + shipping;
            if (totalEl) totalEl.textContent = '₹' + total.toFixed(2);
        }
    })
    .catch(error => console.error("Error loading order summary:", error));
}

// ===== CHATBOT FUNCTIONALITY =====
function sendMessage() {
    var userInput = document.getElementById("user-input");
    var message = userInput.value.trim();
    
    if (message === "") {
        alert("Please type a message!");
        return;
    }

    var chatBox = document.getElementById("chat-box");

    // Display user message
    var userMsg = document.createElement("p");
    userMsg.innerHTML = "<strong>You:</strong> " + escapeHtml(message);
    userMsg.style.color = "#4CAF50";
    userMsg.style.textAlign = "right";
    chatBox.appendChild(userMsg);

    // Show loading indicator
    var loadingMsg = document.createElement("p");
    loadingMsg.innerHTML = "<strong>Bot:</strong> <em>Typing...</em>";
    loadingMsg.id = "loading-msg";
    chatBox.appendChild(loadingMsg);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send to backend API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading indicator
        var loading = document.getElementById("loading-msg");
        if (loading) loading.remove();

        if (data.success) {
            var botMsg = document.createElement("p");
            botMsg.innerHTML = "<strong>Bot:</strong> " + data.response.replace(/\n/g, '<br>');
            botMsg.style.color = "#333";
            chatBox.appendChild(botMsg);
        } else {
            var errorMsg = document.createElement("p");
            errorMsg.innerHTML = "<strong>Bot:</strong> <em>Sorry, something went wrong. Please try again.</em>";
            errorMsg.style.color = "red";
            chatBox.appendChild(errorMsg);
        }

        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        var loading = document.getElementById("loading-msg");
        if (loading) loading.remove();

        var errorMsg = document.createElement("p");
        errorMsg.innerHTML = "<strong>Bot:</strong> <em>Connection error. Please check your internet.</em>";
        errorMsg.style.color = "red";
        chatBox.appendChild(errorMsg);
    });

    // Clear input
    userInput.value = "";
    userInput.focus();
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
    var userInput = document.getElementById("user-input");
    if (userInput) {
        userInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

// ===== MARKETPLACE FUNCTIONS =====

// Load products in marketplace
function loadProducts(category = null) {
    var url = '/api/products';
    if (category) {
        url += '?category=' + encodeURIComponent(category);
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayProducts(data.products);
        } else {
            console.error("Error loading products:", data.error);
        }
    })
    .catch(error => console.error("Fetch error:", error));
}

// Display products dynamically
function displayProducts(products) {
    var productsContainer = document.querySelector('.products');
    if (!productsContainer) return;

    // Clear existing products
    var oldCards = productsContainer.querySelectorAll('.product-card');
    oldCards.forEach(card => card.remove());

    // Add new products
    products.forEach(product => {
        var card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-image">${product.image}</div>
            <h3>${escapeHtml(product.name)}</h3>
            <p class="price">₹${product.price}</p>
            <p class="category">${escapeHtml(product.category)}</p>
            <button onclick="addToCartQuick('${product.id}', '${escapeHtml(product.name)}', ${product.price})">Add to Cart</button>
        `;
        productsContainer.appendChild(card);
    });
}

// ===== PAGE INITIALIZATION =====

// Load products on marketplace page
window.addEventListener('load', function() {
    if (document.querySelector('.products')) {
        loadProducts();
    }
    // Update cart count on every page load
    updateCartCount();
});
