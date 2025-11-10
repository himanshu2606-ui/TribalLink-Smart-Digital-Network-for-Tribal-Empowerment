# Backend by Himanshu Choudhary
# Team TechTribe - Pemiya Rishikesh Institute of Technology

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
                                        
# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for marketplace
@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

# Route for chatbot
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Optional API route for chatbot (if you want to extend real-time backend responses)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get("message", "").lower()
    if "paddy" in user_input or "rice" in user_input:
        response = "Paddy (rice) can be grown in wetland areas. Use organic fertilizers for better yield."
    elif "bamboo" in user_input:
        response = "Bamboo grows fast and can be harvested sustainably. Ideal for handicrafts."
    elif "market" in user_input:
        response = "Visit our Marketplace to explore tribal products!"
    else:
        response = "Sorry, I can only provide basic farming tips or product info for now."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

