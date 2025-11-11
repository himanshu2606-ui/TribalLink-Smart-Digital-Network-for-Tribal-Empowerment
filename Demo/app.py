# Backend by Himanshu Choudhary
# Team TechTribe - Pemiya Rishikesh Institute of Technology

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample product database
PRODUCTS = [
    {"id": 1, "name": "Handmade Bamboo Basket", "price": 250, "category": "Crafts", "image": "🧺"},
    {"id": 2, "name": "Tribal Beaded Necklace", "price": 400, "category": "Jewelry", "image": "📿"},
    {"id": 3, "name": "Clay Pottery", "price": 300, "category": "Pottery", "image": "🏺"},
    {"id": 4, "name": "Organic Rice (1kg)", "price": 150, "category": "Agriculture", "image": "🌾"},
    {"id": 5, "name": "Bamboo Furniture", "price": 2500, "category": "Furniture", "image": "🪑"},
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

# API route for chatbot response with better logic
@app.route('/api/chat', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"success": False, "error": "No message provided"}), 400
        
        user_input = data.get("message", "").strip().lower()
        
        if not user_input:
            return jsonify({"success": False, "error": "Message cannot be empty"}), 400
        
        logger.info(f"Chat message received: {user_input}")
        
        # Enhanced chatbot logic
        response = process_chat_input(user_input)
        
        return jsonify({"success": True, "response": response})
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({"success": False, "error": "Server error"}), 500

def process_chat_input(user_input):
    """Process user input and return appropriate response"""
    keywords = {
        "paddy rice wheat grain": "Paddy (rice) can be grown in wetland areas. Use organic fertilizers for better yield. Best season: May-June.",
        "bamboo craft": "Bamboo grows fast and can be harvested sustainably. Ideal for handicrafts, furniture, and construction.",
        "market product buy sell": "Visit our Marketplace to explore tribal products! We offer authentic handmade items from our community.",
        "price cost rupees": "Our products range from ₹150 to ₹2500. Check the Marketplace for details.",
        "help support question": "I'm here to help! Ask me about farming, products, or visit the Marketplace.",
        "hello hi greet": "Welcome to TribalLink! How can I assist you today?",
    }
    
    # Check for keyword matches
    for keywords_group, response in keywords.items():
        if any(keyword in user_input for keyword in keywords_group.split()):
            return response
    
    # Default response
    return "I can help with farming tips, product info, or marketplace queries. What would you like to know?"

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

