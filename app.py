from flask import Flask, request, jsonify
import requests
import random
import os

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

darkness = 0.0

def call_ai(prompt):
    try:
        r = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 60}
        }, timeout=10)

        data = r.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

    except:
        return ""

    return ""

@app.route("/")
def home():
    return """
    <h2>AI RPG 🖤</h2>
    <input id='msg'>
    <button onclick='send()'>Send</button>
    <pre id='log'></pre>

    <script>
    async function send(){
        let msg = document.getElementById('msg').value
        let res = await fetch('/play', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({msg})
        })
        let data = await res.json()
        document.getElementById('log').textContent += "\\n" + data.reply
    }
    </script>
    """

@app.route("/play", methods=["POST"])
def play():
    global darkness

    user_input = request.json.get("msg")

    darkness += random.uniform(0.05, 0.15)
    darkness = min(darkness, 1.0)

    prompt = f"黑暗戀愛RPG 玩家:{user_input} 黑化值:{darkness} NPC回一句"

    reply = call_ai(prompt)

    if not reply:
        if darkness < 0.5:
            reply = "她冷冷看著你：「你靠太近了。」"
        else:
            reply = "她抓住你：「你走不了。」"

    return jsonify({
        "reply": reply,
        "darkness": darkness
    })

app.run(host="0.0.0.0", port=10000)
