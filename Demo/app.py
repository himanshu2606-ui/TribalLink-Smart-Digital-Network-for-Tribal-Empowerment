# Backend by Himanshu Choudhary & Team TechTribe
# Team TechTribe - Pemiya Rishikesh Institute of Technology
# Upgraded multi-page marketplace + chatbot application

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import logging
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.secret_key = 'triballink-secret-key-2025'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced product database with detailed info
PRODUCTS = [
    {
        "id": 1, 
        "name": "Handmade Bamboo Basket", 
        "price": 250, 
        "category": "Crafts", 
        "image": "🧺",
        "artisan": "Rama Devi",
        "location": "Jharkhand",
        "rating": 4.8,
        "reviews": 245,
        "description": "Beautiful handwoven bamboo basket made by tribal artisans. Perfect for storage and decoration.",
        "details": "Material: Bamboo, Dimensions: 30x20cm, Weight: 500g, Handmade"
    },
    {
        "id": 2, 
        "name": "Tribal Beaded Necklace", 
        "price": 400, 
        "category": "Jewelry", 
        "image": "📿",
        "artisan": "Priya Sharma",
        "location": "Chhattisgarh",
        "rating": 4.9,
        "reviews": 156,
        "description": "Traditional tribal beaded necklace with authentic patterns and colors.",
        "details": "Material: Natural beads + thread, Length: 45cm, Traditional design"
    },
    {
        "id": 3, 
        "name": "Clay Pottery", 
        "price": 300, 
        "category": "Pottery", 
        "image": "🏺",
        "artisan": "Govind Rao",
        "location": "Odisha",
        "rating": 4.7,
        "reviews": 89,
        "description": "Hand-sculpted clay pottery with tribal motifs and traditional techniques.",
        "details": "Material: Clay, Height: 25cm, Handcrafted, Food-safe"
    },
    {
        "id": 4, 
        "name": "Organic Rice (1kg)", 
        "price": 150, 
        "category": "Agriculture", 
        "image": "🌾",
        "artisan": "Farmer's Collective",
        "location": "Jharkhand",
        "rating": 4.6,
        "reviews": 512,
        "description": "Pure organic rice cultivated using traditional tribal farming methods.",
        "details": "Type: Basmati, Weight: 1kg, Organic certified, No pesticides"
    },
    {
        "id": 5, 
        "name": "Bamboo Furniture", 
        "price": 2500, 
        "category": "Furniture", 
        "image": "🪑",
        "artisan": "Master Craftsman Rajesh",
        "location": "Jharkhand",
        "rating": 4.9,
        "reviews": 78,
        "description": "Eco-friendly bamboo chair/table handcrafted with sustainable bamboo.",
        "details": "Material: Bamboo wood, Dimensions: 80x40x40cm, Weight: 4kg, Sustainable"
    },
    {
        "id": 6,
        "name": "Tribal Woven Carpet",
        "price": 1200,
        "category": "Crafts",
        "image": "🧶",
        "artisan": "Lakshmi Weaver Group",
        "location": "Telangana",
        "rating": 4.7,
        "reviews": 156,
        "description": "Hand-woven carpet with authentic tribal patterns using natural dyes.",
        "details": "Size: 150x100cm, Material: Cotton + wool, Handwoven, Durable"
    },
    {
        "id": 7,
        "name": "Tribal Silver Bracelet",
        "price": 550,
        "category": "Jewelry",
        "image": "💍",
        "artisan": "Sumitra Silversmith",
        "location": "Rajasthan",
        "rating": 4.8,
        "reviews": 234,
        "description": "Handcrafted silver bracelet with tribal designs and patterns.",
        "details": "Material: 92.5% Silver, Weight: 45g, Traditional design, Hallmarked"
    },
    {
        "id": 8,
        "name": "Turmeric Powder (500g)",
        "price": 180,
        "category": "Agriculture",
        "image": "🌿",
        "artisan": "Organic Farmers",
        "location": "Jharkhand",
        "rating": 4.6,
        "reviews": 345,
        "description": "Pure organic turmeric powder from tribal farms, no additives.",
        "details": "Weight: 500g, Pure organic, High curcumin content, No preservatives"
    },
]

# Route for homepage
@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template('index.html')

# Route for marketplace
@app.route('/marketplace')
def marketplace():
    logger.info("Marketplace page accessed")
    return render_template('marketplace.html')

# Route for product detail
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    logger.info(f"Product detail page accessed: {product_id}")
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return render_template('product-detail.html', product=product)
    return render_template('error.html', message="Product not found"), 404

# Route for shopping cart
@app.route('/cart')
def cart():
    logger.info("Cart page accessed")
    return render_template('cart.html')

# Route for checkout
@app.route('/checkout')
def checkout():
    logger.info("Checkout page accessed")
    return render_template('checkout.html')

# Route for About page
@app.route('/about')
def about():
    logger.info("About page accessed")
    return render_template('about.html')

# Route for Contact page
@app.route('/contact')
def contact_page():
    logger.info("Contact page accessed")
    return render_template('contact.html')

# Route for chatbot
@app.route('/chatbot')
def chatbot():
    logger.info("Chatbot page accessed")
    return render_template('chatbot.html')

# API route for fetching all products
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category = request.args.get('category', None)
        if category:
            filtered = [p for p in PRODUCTS if p['category'].lower() == category.lower()]
            return jsonify({"success": True, "products": filtered})
        return jsonify({"success": True, "products": PRODUCTS})
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for fetching single product
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = next((p for p in PRODUCTS if p['id'] == product_id), None)
        if product:
            return jsonify({"success": True, "product": product})
        return jsonify({"success": False, "error": "Product not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for cart operations (session-based)
@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def manage_cart():
    try:
        if 'cart' not in session:
            session['cart'] = []
        
        if request.method == 'GET':
            # Return current cart
            return jsonify({"success": True, "cart": session['cart']})
        
        elif request.method == 'POST':
            # Add item to cart
            data = request.get_json()
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            product = next((p for p in PRODUCTS if p['id'] == product_id), None)
            if not product:
                return jsonify({"success": False, "error": "Product not found"}), 404
            
            # Check if already in cart
            cart_item = next((item for item in session['cart'] if item['id'] == product_id), None)
            if cart_item:
                cart_item['quantity'] += quantity
            else:
                session['cart'].append({
                    'id': product_id,
                    'name': product['name'],
                    'price': product['price'],
                    'image': product['image'],
                    'quantity': quantity
                })
            
            session.modified = True
            return jsonify({"success": True, "message": "Item added to cart", "cart": session['cart']})
        
        elif request.method == 'DELETE':
            # Remove item from cart
            data = request.get_json()
            product_id = data.get('product_id')
            session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
            session.modified = True
            return jsonify({"success": True, "message": "Item removed from cart", "cart": session['cart']})
    
    except Exception as e:
        logger.error(f"Error managing cart: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for checkout/payment (Razorpay simulation)
@app.route('/api/checkout', methods=['POST'])
def checkout_payment():
    try:
        data = request.get_json()
        customer_name = data.get('name', 'Customer')
        customer_email = data.get('email', 'customer@example.com')
        customer_phone = data.get('phone', '+91XXXXXXXXXX')
        total_amount = data.get('total_amount', 0)
        
        if not session.get('cart'):
            return jsonify({"success": False, "error": "Cart is empty"}), 400
        
        # Razorpay sandbox simulation
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Checkout: Order {order_id} for {customer_name}, Amount: ₹{total_amount}")
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "amount": total_amount,
            "currency": "INR",
            "customer": {
                "name": customer_name,
                "email": customer_email,
                "phone": customer_phone
            },
            "razorpay_key": "rzp_test_abc123xyz"  # Demo key
        })
    except Exception as e:
        logger.error(f"Error in checkout: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for payment success
@app.route('/api/payment-success', methods=['POST'])
def payment_success():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        logger.info(f"Payment successful for order: {order_id}")
        
        # Clear cart after successful payment
        session['cart'] = []
        session.modified = True
        
        return jsonify({
            "success": True,
            "message": "Payment successful",
            "order_id": order_id
        })
    except Exception as e:
        logger.error(f"Error in payment success: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for contact form
@app.route('/api/contact', methods=['POST'])
def contact_submit():
    try:
        data = request.get_json()
        name = data.get('name', 'Anonymous')
        email = data.get('email', 'no-email')
        message = data.get('message', '')
        
        if not message:
            return jsonify({"success": False, "error": "Message cannot be empty"}), 400
        
        # Log contact message (in real app, send email or store in DB)
        logger.info(f"Contact form: From {name} ({email}) - Message: {message[:100]}")
        
        return jsonify({
            "success": True,
            "message": "Thank you for your message! We'll get back to you soon."
        })
    except Exception as e:
        logger.error(f"Error in contact form: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# API route for chatbot response with multi-language support
@app.route('/api/chat', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"success": False, "error": "No message provided"}), 400
        
        user_input = data.get("message", "").strip().lower()
        language = data.get("language", "en")
        
        if not user_input:
            return jsonify({"success": False, "error": "Message cannot be empty"}), 400
        
        # Store language in session
        session['language'] = language
        session.modified = True
        
        logger.info(f"Chat message received [{language}]: {user_input}")
        
        # Enhanced multi-language chatbot logic
        response = process_chat_input(user_input)
        
        return jsonify({"success": True, "response": response})
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({"success": False, "error": "Server error"}), 500

def process_chat_input(user_input):
    """Process user input with multi-language support (English, Hindi, Santhali, Mundari, Ho)"""
    
    # Multi-language knowledge base
    knowledge_base = {
        'en': {
            # Farming & Agriculture
            "farming agriculture paddy rice wheat grain cultivation": (
                "🌾 **Farming Tips**: Paddy (rice) grows best in wetland areas. "
                "Use organic fertilizers like compost and neem cake. "
                "Best planting season: May-June. Water management is crucial. "
                "Avoid chemical pesticides - use natural pest control methods."
            ),
            "bamboo crop sustainable farming harvest": (
                "🎋 **Bamboo Farming**: Bamboo grows quickly (3-5 years) and is highly sustainable. "
                "It prevents soil erosion and requires minimal pesticides. "
                "Ideal for tribal communities - low cost, high return. "
                "Can be harvested multiple times from same plant."
            ),
            "turmeric spice organic health benefits": (
                "🌿 **Turmeric Benefits**: Our organic turmeric is rich in curcumin (anti-inflammatory). "
                "Used in traditional tribal medicine for centuries. "
                "Perfect for cooking, health supplements, and beauty products. "
                "₹180 for 500g, no additives or preservatives."
            ),
            "marketplace product tribal crafts jewelry furniture": (
                "🛍️ **Our Marketplace**: We have 8+ authentic tribal products: "
                "Handwoven baskets, beaded jewelry, clay pottery, organic rice, bamboo furniture, woven carpets, silver bracelets, and turmeric. "
                "All made by tribal artisans from Jharkhand, Chhattisgarh, Odisha, and other regions. "
                "Fair prices, 100% authentic, direct from makers."
            ),
            "price cost rupees payment checkout cart": (
                "💰 **Pricing**: Our products range from ₹150 (rice) to ₹2500 (furniture). "
                "Browse the Marketplace to see all prices. Add to cart and checkout. "
                "We accept UPI, cards, and wallets."
            ),
            "government scheme tribal assistance benefits welfare": (
                "📋 **Government Support**: Schemes for tribal communities: "
                "1. PM Jati Adharsh Gram - ₹50 lakh per village "
                "2. National Tribal Fellowship - higher education "
                "3. Gram Samriddhi Yojana - village development "
                "Contact your local Gram Panchayat."
            ),
            "skill development training education learning program": (
                "📚 **Skill Training**: TribalLink offers: Digital literacy, Handicraft training, "
                "Agricultural workshops, E-commerce & marketing skills. "
                "Ask for programs in your area!"
            ),
            "hello hi greet welcome": (
                "👋 **Welcome to TribalLink!** I'm AgriHelp Bot. "
                "I can help with farming, products, schemes, and training. What would you like?"
            ),
        },
        'hi': {
            "farming agriculture paddy rice wheat grain cultivation": (
                "🌾 **खेती सुझाव**: धान (चावल) गीली भूमि में अच्छी तरह उगता है। "
                "खाद और नीम केक का उपयोग करें। बुवाई का मौसम मई-जून है। "
                "पानी का प्रबंधन महत्वपूर्ण है। रासायनिक कीटनाशकों से बचें।"
            ),
            "bamboo crop sustainable farming harvest": (
                "🎋 **बांस की खेती**: बांस 3-5 साल में तेजी से बढ़ता है। "
                "यह मिट्टी के कटाव को रोकता है और कम कीटनाशकों की जरूरत है। "
                "आदिवासी समुदायों के लिए कम लागत, अधिक लाभ। "
                "एक ही पौधे से कई बार कटाई की जा सकती है।"
            ),
            "turmeric spice organic health benefits": (
                "🌿 **हल्दी के लाभ**: हमारी जैविक हल्दी करक्यूमिन से भरपूर है। "
                "सदियों से आदिवासी चिकित्सा में प्रयुक्त होती है। "
                "खाना पकाने, स्वास्थ्य और सौंदर्य के लिए बेहतरीन। "
                "500ग्राम ₹180, कोई योगज नहीं।"
            ),
            "hello hi greet welcome": (
                "👋 **TribalLink में आपका स्वागत है!** मैं AgriHelp बॉट हूं। "
                "मैं खेती, उत्पाद, योजनाओं और प्रशिक्षण में मदद कर सकता हूं। "
                "आप क्या जानना चाहते हैं?"
            ),
        },
        'san': {
            "farming agriculture paddy rice wheat grain cultivation": (
                "� **खेती के सुझाव**: धान जलभूमि में अच्छी तरह उगता है। "
                "खाद का उपयोग करें। कीटनाशकों से बचें। मई-जून बुवाई का समय है।"
            ),
            "hello hi greet welcome": (
                "👋 **TribalLink में आपका स्वागत है!** मैं आपकी मदद कर सकता हूं। "
                "खेती, पणय, योजना के बारे में पूछें।"
            ),
        },
        'mun': {
            "farming agriculture paddy rice wheat grain cultivation": (
                "🌾 **खेती**: धान गीली जमीन में अच्छी तरह बढ़ता है। "
                "खाद डालब, जहर मत डालब। मई-जून में बुवाई करब।"
            ),
            "hello hi greet welcome": (
                "👋 **TribalLink में आपका स्वागत!** मैं आपकी मदद कर सकता हूं। "
                "खेती, सामान के बारे में पूछें।"
            ),
        },
        'ho': {
            "farming agriculture paddy rice wheat grain cultivation": (
                "🌾 **Farming**: Rice grows well in wet land. Use compost. "
                "No poison. Plant in May-June."
            ),
            "hello hi greet welcome": (
                "👋 **Welcome to TribalLink!** I can help you. "
                "Ask about farming, products, schemes."
            ),
        }
    }
    
    # Detect language from session or default to English
    detected_lang = session.get('language', 'en')
    user_lower = user_input.lower()
    
    # Check if user is asking in a specific language (simple detection)
    hindi_keywords = ['कैसे', 'क्या', 'किसे', 'कहां', 'कब']
    if any(keyword in user_input for keyword in hindi_keywords):
        detected_lang = 'hi'
        session['language'] = 'hi'
    
    # Search for matching topics in detected language
    lang_kb = knowledge_base.get(detected_lang, knowledge_base['en'])
    
    for keywords, response in lang_kb.items():
        if any(keyword in user_lower for keyword in keywords.split()):
            return response
    
    # Multi-language fallback responses
    fallbacks = {
        'en': (
            "ℹ️ **I can help with**: 🌾 Farming tips, 🛍️ Products, "
            "💰 Payment, 📚 Training, 📋 Schemes, 🆘 Support\n"
            "Try: 'How to grow rice?', 'Tell about products', 'What schemes?'"
        ),
        'hi': (
            "ℹ️ **मैं मदद कर सकता हूं**: 🌾 खेती, 🛍️ उत्पाद, "
            "💰 भुगतान, 📚 प्रशिक्षण, 📋 योजनाएं, 🆘 समर्थन\n"
            "पूछें: 'धान कैसे उगाएं?', 'उत्पाद बताएं', 'कौन सी योजनाएं?'"
        ),
        'san': (
            "ℹ️ **मैं मदद कर सकता हूं**: 🌾 खेती, 🛍️ पणय, "
            "� भुगतान, �📚 प्रशिक्षण, 📋 योजना\n"
            "पूछें: खेती, पणय, योजना के बारे में।"
        ),
        'mun': (
            "ℹ️ **मैं मदद कर सकता हूं**: 🌾 खेती, 🛍️ सामान, "
            "� भुगतान, 📚 सीखब, �📋 योजना\n"
            "पूछब: खेती, सामान, योजना।"
        ),
        'ho': (
            "ℹ️ **I can help**: 🌾 Farming, 🛍️ Products, "
            "💰 Payment, 📚 Training, 📋 Schemes\n"
            "Ask: about farming, products, schemes."
        )
    }
    
    return fallbacks.get(detected_lang, fallbacks['en'])

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

