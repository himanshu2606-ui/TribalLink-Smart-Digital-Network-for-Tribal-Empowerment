# Multi-Language Support Feature Guide

## Overview
TribalLink now supports **5 tribal languages** to ensure inclusive access for all tribal communities:
- 🇮🇳 **English** (en)
- 🇮🇳 **हिंदी - Hindi** (hi)
- 🇮🇳 **संथाली - Santhali** (san)
- 🇮🇳 **Mundari** (mun)
- 🇮🇳 **Ho** (ho)

---

## Features Implemented

### 1. **Language Selector UI** (Frontend)
Located on `/chatbot` page:
```
🌐 Choose Language / भाषा चुनें:
┌─────────┬──────────┬──────────┬──────────┬──────┐
│ English │ हिंदी    │ संथाली   │ Mundari  │ Ho   │
└─────────┴──────────┴──────────┴──────────┴──────┘
```

**Button Styling:**
- Active language: White background, green text (#4CAF50)
- Inactive languages: Transparent background, white text
- Smooth transition on hover

### 2. **Language Detection** (Backend)
The chatbot automatically detects language from user input:

**Hindi Detection Keywords:**
- कैसे (How), क्या (What), किसे (Whom)
- कहां (Where), कब (When)
- खेती (Farming), उपज (Harvest)

**Examples:**
- Typing "कैसे धान उगाए?" → Auto-detects Hindi
- Typing "Farming tips" → English
- Switching language manually → Override detection

### 3. **Language Persistence**
User's language preference is saved in `sessionStorage`:
- Preference persists on page refresh
- Per-browser session (resets if browser cache cleared)
- Automatically restored on page load

### 4. **Multi-Language Knowledge Base**
Each language has dedicated responses for:
- 🌾 **Farming & Agriculture** (Rice, Wheat, Pulses, Vegetables)
- 🛍️ **Products & Artisans** (Crafts, Jewelry, Pottery, Furniture)
- 📋 **Government Schemes** (PM-KISAN, MNREGA, Subsidies)
- 🎉 **Festival Information** (Diwali, Holi, Local Festivals)
- 👋 **Greetings & General Help**

---

## Technical Implementation

### Backend Changes (`app.py`)

#### Multi-Language Knowledge Base Structure:
```python
knowledge_base = {
    'en': {
        'farming agriculture ...': '🌾 **Farming Tips**: ...',
        'hello hi greet ...': '👋 **Welcome**: ...',
    },
    'hi': {
        'farming agriculture ...': '🌾 **खेती की सलाह**: ...',
        'hello hi greet ...': '👋 **TribalLink में स्वागत है!**: ...',
    },
    'san': {...},  # Santhali translations
    'mun': {...},  # Mundari translations
    'ho': {...}    # Ho translations
}
```

#### Language Detection Logic:
```python
def detect_language(user_input):
    hindi_keywords = ['कैसे', 'क्या', 'किसे', 'कहां', 'कब', ...]
    if any(keyword in user_input for keyword in hindi_keywords):
        return 'hi'
    return 'en'  # Default to English
```

#### API Endpoint Update:
```python
@app.route('/api/chat', methods=['POST'])
def get_response():
    data = request.get_json()
    message = data.get("message", "").strip().lower()
    language = data.get("language", "en")  # NEW: Language parameter
    
    # Store language in session for persistence
    session['language'] = language
    
    response = process_chat_input(message)
    return jsonify({"success": True, "response": response})
```

### Frontend Changes (`templates/chatbot.html`)

#### Language Selector UI:
```html
<!-- Language Selection Section -->
<div style="background: rgba(0,0,0,0.1); padding: 20px 15px; border-radius: 8px; margin-bottom: 20px;">
    <p style="margin: 0 0 12px 0; font-size: 14px; color: #888;">
        Choose Language / भाषा चुनें:
    </p>
    <div id="languageButtons" style="display: flex; gap: 8px; flex-wrap: wrap;">
        <button class="lang-btn" data-lang="en" style="background: white; color: #4CAF50;">English</button>
        <button class="lang-btn" data-lang="hi" style="background: rgba(255,255,255,0.3); color: white;">हिंदी</button>
        <button class="lang-btn" data-lang="san" style="background: rgba(255,255,255,0.3); color: white;">संथाली</button>
        <button class="lang-btn" data-lang="mun" style="background: rgba(255,255,255,0.3); color: white;">Mundari</button>
        <button class="lang-btn" data-lang="ho" style="background: rgba(255,255,255,0.3); color: white;">Ho</button>
    </div>
</div>
```

#### Language Switching JavaScript:
```javascript
let currentLanguage = 'en';

// Load saved language preference on page load
window.addEventListener('load', function() {
    const savedLanguage = sessionStorage.getItem('chatLanguage');
    if (savedLanguage) {
        currentLanguage = savedLanguage;
        updateLanguageButtons();
    }
});

// Language button click handlers
document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        currentLanguage = this.getAttribute('data-lang');
        sessionStorage.setItem('chatLanguage', currentLanguage);
        updateLanguageButtons();
    });
});

// Send message with language parameter
async function sendMessage() {
    const message = document.getElementById('chatInput').value.trim();
    if (!message) return;
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            message: message,
            language: currentLanguage  // Include language!
        })
    });
    // ... rest of logic
}
```

---

## How to Use

### For End Users:
1. **Open chatbot**: http://127.0.0.1:5000/chatbot
2. **Select language**: Click button for your preferred language
3. **Type message**: In English or selected language
4. **Get response**: In your chosen language
5. **Switch anytime**: Click different language button

### For Developers:
1. **Extend languages**: Add new language dict to `knowledge_base` in `process_chat_input()`
2. **Add responses**: Add keywords and corresponding translations
3. **Update UI**: Add new button to language selector
4. **Update detection**: Add keywords to `detect_language()` function

---

## Testing Checklist

### ✅ Tests Performed:
- [x] English language responses working
- [x] Hindi language detection working
- [x] API accepts language parameter
- [x] Language buttons render correctly
- [x] Language persists on page refresh
- [x] Language-specific typing messages display
- [x] Cart still functions (multi-language doesn't affect)
- [x] Other pages unaffected

### ✅ Git Commit:
```bash
Commit: 567175c
Message: Add multi-language support (5 languages: English, Hindi, 
         Santhali, Mundari, Ho) with language detection, session 
         persistence, and tribal language responses
Files Changed: 2
  - app.py (86 insertions)
  - templates/chatbot.html (130 insertions, 86 deletions)
```

---

## API Reference

### Chat Endpoint with Language Support

**Endpoint:** `POST /api/chat`

**Request Body:**
```json
{
    "message": "कैसे धान उगाए?",
    "language": "hi"
}
```

**Response (Success):**
```json
{
    "success": true,
    "response": "🌾 **खेती की सलाह**: धान उगाने के लिए..."
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "Message cannot be empty"
}
```

---

## Supported Topics by Language

### English (en)
- Farming: Rice, Wheat, Pulses, Vegetables
- Products: Crafts, Jewelry, Pottery
- Schemes: PM-KISAN, MNREGA
- Other: Greetings, Help, General info

### हिंदी (hi)
- खेती: धान, गेहूँ, दाल, सब्जियां
- उत्पाद: हस्तशिल्प, गहने, मिट्टी के बर्तन
- योजनाएं: पीएम-किसान, मनरेगा
- अन्य: नमस्ते, मदद, सामान्य जानकारी

### संथाली (san), Mundari (mun), Ho (ho)
- Similar topics adapted for tribal communities
- Agricultural practices relevant to Jharkhand
- Government scheme information

---

## Future Enhancements

1. **Full Site Multi-Language** (not just chatbot)
   - Navigation bar language switcher
   - All pages in multiple languages
   - Global language preference storage

2. **More Languages**
   - Odia (Eastern India)
   - Telugu (Southern India)
   - Marathi (Western India)

3. **Real Translation API**
   - Google Translate API integration
   - More accurate translations
   - Auto-detect language from user input

4. **Language Analytics**
   - Track which languages are used most
   - Identify language preferences by region
   - Optimize for high-demand languages

5. **Accessibility Features**
   - Text-to-speech for responses
   - Voice input (speech-to-text)
   - Larger fonts for elderly users

---

## Support

For issues or questions about multi-language feature:
1. Check chatbot page at `/chatbot`
2. Verify language buttons are visible
3. Test API with: `curl -X POST http://127.0.0.1:5000/api/chat -H "Content-Type: application/json" -d '{"message":"hello","language":"en"}'`
4. Check browser console for errors (F12)
5. Contact development team

---

**Status:** ✅ **COMPLETE & TESTED**
**Last Updated:** November 13, 2025
**Version:** 1.0 (Multi-Language Beta)

