from flask import Flask, request, jsonify
from openai import OpenAI
import random
from db import *

app = Flask(__name__)
client = OpenAI()

init_db()

@app.route("/")
def home():
    return """
    <h2>AI RPG 🖤</h2>
    <input id='msg' placeholder='輸入...'>
    <button onclick='send()'>發送</button>
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
        document.getElementById('log').innerText += "\\n" + data.reply
    }
    </script>
    """

@app.route("/play", methods=["POST"])
def play():
    user_input = request.json.get("msg")

    save_memory(user_input)
    memory = get_memory()

    darkness = get_darkness()
    darkness += random.uniform(0.05, 0.15)
    darkness = min(darkness, 1.0)
    update_darkness(darkness)

    prompt = f"""
    黑暗戀愛RPG

    玩家: {user_input}
    記憶: {memory}
    黑化值: {darkness}

    NPC1 冷淡控制型一句
    NPC2 危險誘惑型一句
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = res.choices[0].message.content

    return jsonify({
        "reply": text,
        "darkness": darkness,
        "memory": memory
    })

app.run(host="0.0.0.0", port=10000)
