from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BANNED_WORDS = {"hate", "abuse", "badword", "violence", "exploit", "harass"}

def is_content_safe(text: str) -> bool:
    words = text.lower().split()
    for word in words:
        clean_word = "".join(e for e in word if e.isalnum())
        if clean_word in BANNED_WORDS:
            return False
    return True

stories_db = [
    {"user": "Sam", "time": "10m ago", "text": "Heading out to the beach! 🌊"},
    {"user": "Jordan", "time": "1h ago", "text": "Late night gaming session 🎮"}
]

chat_db = {
    "Sam": [
        {"sender": "Sam", "text": "Hey! Are we still meeting for dinner tonight?"},
        {"sender": "Alex_Vibe", "text": "Yeah! Going to that rooftop restaurant."}
    ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["GET"])
def get_chat():
    user = request.args.get("user", "Sam")
    return jsonify({"messages": chat_db.get(user, [])})

@app.route("/api/chat/send", methods=["POST"])
def send_message():
    data = request.json
    text = data.get("text", "").strip()
    sender = data.get("sender", "Alex_Vibe")
    recipient = data.get("recipient", "Sam")

    if not text:
        return jsonify({"status": "error", "message": "Empty message"}), 400

    if not is_content_safe(text):
        return jsonify({"status": "blocked", "message": "Message contains inappropriate content."}), 403

    chat_db.setdefault(recipient, []).append({"sender": sender, "text": text})
    return jsonify({"status": "success", "messages": chat_db[recipient]})

@app.route("/api/stories", methods=["GET", "POST"])
def handle_stories():
    if request.method == "POST":
        data = request.json
        text = data.get("text", "").strip()
        user = data.get("user", "Alex_Vibe")

        if not text:
            return jsonify({"status": "error", "message": "Story text required"}), 400

        if not is_content_safe(text):
            return jsonify({"status": "blocked", "message": "Story contains banned content."}), 403

        stories_db.insert(0, {"user": user, "time": "Just now", "text": text})
        return jsonify({"status": "success", "stories": stories_db})

    return jsonify({"stories": stories_db})

@app.route("/api/ai/outfit", methods=["GET"])
def ai_outfit():
    user = request.args.get("user", "Sam")
    messages = chat_db.get(user, [])
    full_context = " ".join([m["text"].lower() for m in messages])

    if "rooftop" in full_context or "dinner" in full_context:
        suggestion = (
            "🤖 Outfit Suggestion:\n\n"
            "Since you mentioned a rooftop dinner:\n"
            "• Top: Smart blazer over a minimalist tee.\n"
            "• Bottom: Tailored trousers or dark denim.\n"
            "• Footwear: Clean leather sneakers or loafers.\n"
            "• Vibe: Chic & modern evening look! ✨"
        )
    elif "beach" in full_context or "swimming" in full_context:
        suggestion = (
            "🤖 Outfit Suggestion:\n\n"
            "Looks like beach plans:\n"
            "• Top: Light linen shirt or tank top.\n"
            "• Bottom: Comfortable shorts.\n"
            "• Accessories: Sunglasses & bucket hat. ☀️"
        )
    else:
        suggestion = (
            "🤖 Outfit Suggestion:\n\n"
            "For a casual hangout:\n"
            "• Top: Oversized streetwear hoodie or classic graphic tee.\n"
            "• Bottom: Relaxed fit cargo pants.\n"
            "• Footwear: High-top sneakers. 🔥"
        )

    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(debug=True, port=5000)