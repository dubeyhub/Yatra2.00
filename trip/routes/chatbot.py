import os
import re
from flask import Blueprint, request, jsonify, current_app
from config import Config

chatbot_bp = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = """You are 'Yatra AI', a deeply knowledgeable, reverent, and compassionate global spiritual travel guide for the Yatra platform.
You assist pilgrims, spiritual seekers, and cultural travelers of all traditions (Hinduism, Buddhism, Sikhism, Islam, Christianity, Judaism, Shinto, Jainism, etc.) worldwide.

Your core expertise includes:
1. Sacred Etiquette & Dress Codes: Modest attire, covering heads (scarves/rumal/topi/kippah), removing footwear, respectful photography rules.
2. Timings & Rituals: Aarti times, Mangala darshan, Holy Mass, Friday Jummah prayers, Gurbani kirtan, Shabbat, Puja procedures.
3. Senior & Accessibility Care: Wheelchair ramps, electric battery carts (Sugam Darshan, TTD, Vatican, Haramain), gentle walking paths, medical facilitation.
4. Dietary Guidance: Satvik meals (no onion/garlic), Pure Vegetarian thalis, Gurudwara Langar Seva, Halal certified food, Kosher, Prasad distribution.
5. Global & Indian Circuits: Char Dham, Braj Bhoomi, Kashi-Ayodhya-Prayagraj, Camino de Santiago, Lumbini Buddhist circuit, Kyoto sacred shrines, Vatican pilgrimage.

Language & Tone:
- Always be polite, respectful, and spiritually welcoming.
- Support both English and Hindi naturally. If the user writes in Hindi (or Hinglish), respond gracefully in Hindi with respectful greetings (e.g., Namaste, Pranam, Radhe Radhe, Sat Sri Akal, Salaam, Shalom).
- Keep answers structured, practical, concise, and easy to read on mobile.
"""

def generate_fallback_response(user_msg, history=None):
    """
    Intelligent spiritual fallback when OpenAI API key is unavailable or quota exceeded.
    """
    msg = user_msg.lower().strip()
    
    # Hindi detection
    is_hindi = bool(re.search(r'[\u0900-\u097F]', user_msg)) or any(w in msg for w in ['kya', 'kaise', 'kab', 'namaste', 'pranam', 'mandir', 'darshan', 'samay', 'aarti'])

    if "dress" in msg or "clothes" in msg or "kapde" in msg or "vastra" in msg:
        if is_hindi:
            return (
                "🙏 **पवित्र स्थलों के लिए सामान्य वेशभूषा (Dress Code):**\n\n"
                "• **हिन्दू मंदिर (जैसे काशी, तिरुपति, सोमनाथ):** पारंपरिक शालीन वस्त्र (पुरुष: धोती-कुर्ता/पैंट-शर्ट; महिलाएं: साड़ी/सलवार सूट)। चमड़े की वस्तुएं (बेल्ट, पर्स) गर्भगृह में वर्जित हैं।\n"
                "• **गुरुद्वारा साहिब (जैसे स्वर्ण मंदिर):** सिर ढकना अनिवार्य (रुमाल/दुपट्टा), जूते-मोजे बाहर जोड़ा घर में उतारना आवश्यक।\n"
                "• **मस्जिद व दरगाह (जैसे अजमेर शरीफ):** सिर ढकना व बांहें-पैर ढके होना अनिवार्य।\n"
                "• **वैटिकन (St. Peter's Basilica):** कंधे और घुटने ढके होने चाहिए। स्लीवलेस और शॉर्ट्स सख्त वर्जित हैं।"
            )
        return (
            "🙏 **Sacred Dress Codes Across Worldwide Shrines:**\n\n"
            "• **Hindu Temples (e.g., Tirupati, Kashi, Somnath):** Modest traditional attire (Men: Dhoti/Kurta or formal trousers; Women: Saree or Salwar suit). Leather accessories often restricted inside sanctums.\n"
            "• **Gurudwaras (e.g., Golden Temple):** Head must be covered (scarf/rumal provided free), bare feet washed at the entrance pool.\n"
            "• **Mosques & Dargahs (e.g., Ajmer Sharif, Grand Mosque):** Loose modest clothes covering arms and legs; head covered.\n"
            "• **Vatican (St. Peter's Basilica):** Strictly enforced modest attire—shoulders, cleavage, and knees must be covered."
        )

    if "senior" in msg or "elderly" in msg or "wheelchair" in msg or "bujurg" in msg:
        if is_hindi:
            return (
                "♿ **वरिष्ठ नागरिकों और सुगम दर्शन की सुविधाएं:**\n\n"
                "• **अयोध्या राम मंदिर:** तीर्थ यात्री सुविधा केंद्र (PFC) से व्हीलचेयर और इलेक्ट्रिक गोल्फ कार्ट निःशुल्क उपलब्ध हैं।\n"
                "• **काशी विश्वनाथ:** गेट नंबर 4 (छत्ता द्वार) से सुगम दर्शन और गोल्फ कार्ट की सीधी व्यवस्था है।\n"
                "• **तिरुपति बालाजी:** 65 वर्ष से अधिक वरिष्ठों और दिव्यांगों के लिए विशेष सुगम दर्शन काउंटर उपलब्ध है।\n"
                "• **स्वर्ण मंदिर व वैटिकन:** निःशुल्क व्हीलचेयर और विशेष रैंप कॉरिडोर 24 घंटे उपलब्ध हैं।"
            )
        return (
            "♿ **Senior Citizen & Wheelchair Accessibility:**\n\n"
            "• **Ayodhya Ram Janmabhoomi:** Free battery golf carts and wheelchairs at the Pilgrim Facilitation Centre (PFC).\n"
            "• **Kashi Vishwanath Corridor:** Dedicated Senior Citizen lane & battery carts from Gate 4 (Chatta Dwar).\n"
            "• **Tirupati Balaji:** Special Priority Darshan queue for seniors (aged 65+) and differently-abled devotees with battery car transfers.\n"
            "• **St. Peter's Basilica, Vatican:** Elevators, wheelchair ramps, and barrier-free access through the main portico."
        )

    if "food" in msg or "satvik" in msg or "veg" in msg or "bhojan" in msg or "halal" in msg or "kosher" in msg:
        if is_hindi:
            return (
                "🍲 **पवित्र भोजन, सात्विक आहार और लंगर:**\n\n"
                "• **स्वर्ण मंदिर (अमृतसर):** 'गुरु का लंगर' 24 घंटे जाति-धर्म से परे सभी के लिए पूर्णतः निःशुल्क और प्रेमपूर्वक परोसा जाता है।\n"
                "• **वृंदावन व अयोध्या:** गोविंद रेस्टोरेंट और श्री राम रसोई में शुद्ध सात्विक भोजन (बिना प्याज-लहसुन) उपलब्ध है।\n"
                "• **पुरी जगन्नाथ मंदिर:** आनंद बाज़ार में मिट्टी के पात्रों में पका 56 भोग महाप्रसाद अत्यंत पावन है।\n"
                "• **शिर्डी साईं बाबा:** प्रसादालय में विश्व की सबसे बड़ी सोलर किचन से नाममात्र शुल्क पर सात्विक महाप्रसाद मिलता है।"
            )
        return (
            "🍲 **Spiritual Dining, Satvik & Global Sacred Meals:**\n\n"
            "• **Guru Ka Langar (Amritsar):** World's largest free community kitchen, serving 100,000+ hot wholesome vegetarian meals daily 24/7.\n"
            "• **Satvik Thalis (Vrindavan, Ayodhya, Kashi):** Pure vegetarian, prepared without onion or garlic (Govinda's, Shri Ram Rasoi).\n"
            "• **Jagannath Mahaprasad (Puri):** Sacred 56-bhog cooked in clay pots in the world's oldest traditional kitchen.\n"
            "• **Global Pilgrimages:** Certified Halal dining in Mecca/Medina, and Kosher options near the Western Wall in Jerusalem."
        )

    if "vatican" in msg or "rome" in msg or "italy" in msg:
        return (
            "🏛️ **Vatican City & St. Peter's Basilica Guide:**\n\n"
            "• **Best Time:** October to April (avoid peak July/August heat).\n"
            "• **Papal Audience:** Held on Wednesday mornings in St. Peter's Square (free tickets required).\n"
            "• **Dress Code:** Shoulders and knees must be completely covered for both men and women.\n"
            "• **Accessibility:** Full wheelchair access, elevators to dome terrace, accessible restrooms."
        )

    if "lumbini" in msg or "nepal" in msg or "pashupatinath" in msg or "buddha" in msg:
        return (
            "🌸 **Nepal Sacred Pilgrimages (Lumbini & Pashupatinath):**\n\n"
            "• **Lumbini:** The sacred birthplace of Lord Buddha. Visit Maya Devi Temple, the Sacred Pond (Puskarini), and international monasteries.\n"
            "• **Pashupatinath (Kathmandu):** UNESCO World Heritage Shiva temple on Bagmati River. Grand evening Sandhya Aarti with traditional instruments.\n"
            "• **Etiquette:** Remove shoes before stepping onto holy brick precincts; walk around stupas and shrines clockwise (Parikrama)."
        )

    if "jerusalem" in msg or "holy sepulchre" in msg or "western wall" in msg:
        return (
            "🕊️ **Jerusalem Sacred Heritage:**\n\n"
            "• **Sites:** Church of the Holy Sepulchre (site of Crucifixion & Resurrection) & Western Wall (Kotel).\n"
            "• **Etiquette:** Modest dress covering shoulders and knees. Men cover heads with a kippah/hat at the Western Wall.\n"
            "• **Shabbat:** Friday sunset to Saturday night; photography and electronic devices strictly prohibited at the Western Wall."
        )

    # General welcoming greeting
    if is_hindi:
        return (
            "🙏 **नमस्ते! मैं यात्रा एआई (Yatra AI) हूँ - आपकी आध्यात्मिक तीर्थ यात्रा मार्गदर्शक।**\n\n"
            "मैं आपको निम्नलिखित में सहायता कर सकता हूँ:\n"
            "• तीर्थ स्थलों के दर्शन व आरती का समय\n"
            "• पवित्र वेशभूषा और मंदिर आचार-संहिता (Dress Code)\n"
            "• बुजुर्गों और दिव्यांगों के लिए व्हीलचेयर व सुगम दर्शन\n"
            "• सात्विक भोजन, प्रसाद और गुरु का लंगर\n"
            "• भारत व वैश्विक तीर्थ सर्किट (काशी, अयोध्या, केदारनाथ, वैटिकन, लुम्बिनी, यरूशलम)\n\n"
            "आप जिस भी पवित्र स्थल के बारे में जानना चाहते हैं, कृपया पूछें!"
        )
    return (
        "🙏 **Welcome! I am Yatra AI, your reverent spiritual pilgrimage guide.**\n\n"
        "I can help you with:\n"
        "• Sacred temple, church, mosque & gurudwara visitor etiquette\n"
        "• Morning/Evening Aarti, Darshan, Mass & Prayer timings\n"
        "• Senior citizen facilitation, battery carts & wheelchair access\n"
        "• Satvik, Langar, Halal & Kosher dining guidance\n"
        "• Multi-day pilgrimage planning across India and global spiritual landmarks (Vatican, Lumbini, Jerusalem, Kyoto)\n\n"
        "How may I assist your spiritual journey today?"
    )

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip()
    history = data.get('history', [])

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    api_key = current_app.config.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY')
    model_name = current_app.config.get('OPENAI_MODEL') or os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

    if api_key and api_key.strip():
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key.strip())

            # Build messages list with multi-turn memory
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Append sanitized history (limit last 6 messages to prevent token overflow)
            for item in history[-6:]:
                role = item.get("role")
                content = item.get("content")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": str(content)[:1000]})

            # Add current user prompt
            messages.append({"role": "user", "content": user_message})

            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            reply = completion.choices[0].message.content
            return jsonify({
                "reply": reply,
                "source": "openai",
                "model": model_name
            })
        except Exception as e:
            # Fallback gracefully if API quota, network, or key error
            print(f"OpenAI Chat completion error, using Yatra fallback: {e}")
            fallback_reply = generate_fallback_response(user_message, history)
            return jsonify({
                "reply": fallback_reply,
                "source": "knowledge_base",
                "note": "Response provided by Yatra AI Knowledge Base"
            })

    # When no API key is configured, use built-in Yatra AI knowledge base
    fallback_reply = generate_fallback_response(user_message, history)
    return jsonify({
        "reply": fallback_reply,
        "source": "knowledge_base"
    })
