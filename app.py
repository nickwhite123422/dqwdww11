from flask import Flask, request, jsonify
import openai, os
from pathlib import Path

app = Flask(__name__)
openai.api_key = os.getenv("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
")

# Endpoint for text chat
@app.route("/chat", methods=["POST"])
def chat():
    user_text = request.json.get("text", "")
    if not user_text:
        return jsonify({"error": "No text provided"}), 400
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )
    answer = response.choices[0].message.content
    return jsonify({"reply": answer})

# Endpoint for TTS (optional)
@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    audio_resp = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    audio_file = Path("response.mp3")
    with open(audio_file, "wb") as f:
        f.write(audio_resp.read())
    return jsonify({"message": "Audio generated", "file": "response.mp3"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
