// Frontend JS by Himanshu Choudhary
// Team TechTribe - Pemiya Rishikesh Institute of Technology

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    var chatBox = document.getElementById("chat-box");

    // Display user message
    var userMsg = document.createElement("p");
    userMsg.innerHTML = "<strong>You:</strong> " + userInput;
    chatBox.appendChild(userMsg);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Get bot response (simple keyword-based logic)
    var botResponse = getBotResponse(userInput);

    var botMsg = document.createElement("p");
    botMsg.innerHTML = "<strong>Bot:</strong> " + botResponse;
    chatBox.appendChild(botMsg);

    // Clear input
    document.getElementById("user-input").value = "";
}

// Simple keyword-based responses
function getBotResponse(input) {
    input = input.toLowerCase();
    if (input.includes("paddy") || input.includes("rice")) {
        return "Paddy (rice) can be grown in wetland areas. Use organic fertilizers for better yield.";
    } else if (input.includes("bamboo")) {
        return "Bamboo grows fast and can be harvested sustainably. Ideal for handicrafts.";
    } else if (input.includes("market")) {
        return "Visit our Marketplace to explore tribal products!";
    } else {
        return "Sorry, I can only provide basic farming tips or product info for now.";
    }
}
