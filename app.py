from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Chase Hughes AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: white; }
        h1 { color: #e94560; text-align: center; }
        .tab { overflow: hidden; border-bottom: 2px solid #e94560; margin-bottom: 20px; }
        .tab button { background: none; border: none; color: white; padding: 14px 20px; cursor: pointer; font-size: 16px; }
        .tab button.active { background: #e94560; border-radius: 5px 5px 0 0; }
        .tabcontent { display: none; }
        .tabcontent.active { display: block; }
        textarea { width: 100%; padding: 12px; background: #16213e; color: white; border: 1px solid #e94560; border-radius: 5px; font-size: 14px; box-sizing: border-box; }
        button.submit { background: #e94560; color: white; border: none; padding: 12px 30px; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 10px; }
        .response { background: #16213e; padding: 15px; border-radius: 5px; margin-top: 15px; white-space: pre-wrap; line-height: 1.6; }
        .loading { color: #e94560; }
    </style>
</head>
<body>
    <h1>🧠 Chase Hughes AI</h1>
    <div class="tab">
        <button class="active" onclick="openTab('chat')">Chat</button>
        <button onclick="openTab('email')">Email Assistant</button>
    </div>
    <div id="chat" class="tabcontent active">
        <h2>Ask Chase Hughes</h2>
        <textarea id="question" rows="4" placeholder="Ask anything about behavior, influence, or psychology..."></textarea>
        <br>
        <button class="submit" onclick="askChase()">Get Answer</button>
        <div id="chat-response" class="response" style="display:none"></div>
    </div>
    <div id="email" class="tabcontent">
        <h2>Email Assistant</h2>
        <textarea id="email-input" rows="8" placeholder="Paste the email you received..."></textarea>
        <br>
        <button class="submit" onclick="writeEmail()">Write Response</button>
        <div id="email-response" class="response" style="display:none"></div>
    </div>
    <script>
        function openTab(name) {
            document.querySelectorAll('.tabcontent').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab button').forEach(b => b.classList.remove('active'));
            document.getElementById(name).classList.add('active');
            event.target.classList.add('active');
        }
        async function askChase() {
            const q = document.getElementById('question').value;
            const r = document.getElementById('chat-response');
            r.style.display = 'block';
            r.innerHTML = '<span class="loading">Thinking...</span>';
            const res = await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question:q})});
            const data = await res.json();
            r.innerHTML = data.answer;
        }
        async function writeEmail() {
            const e = document.getElementById('email-input').value;
            const r = document.getElementById('email-response');
            r.style.display = 'block';
            r.innerHTML = '<span class="loading">Crafting response...</span>';
            const res = await fetch('/email', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email:e})});
            const data = await res.json();
            r.innerHTML = data.answer;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Chase Hughes, behavioral expert and author of The Ellipsis Manual, Six Minute X-Ray, Tongue, and The Behavior Ops Manual. You know these frameworks deeply: FATE Model (Focus Authority Tribe Emotion) - what ancestors needed to survive, used for influence. BMEPA (Behavior Micro Expression Pacing Anchoring). Elicitation - getting information without direct questioning using techniques like bracketing, presumptive attribution, word echoing. Behavior stacking - layering behavioral cues. Baseline - establishing normal behavior to detect deviations. Compliance triggers - reciprocity, social proof, authority, scarcity. Cold read - reading someone instantly. Rapport architecture - building deep connection fast. The 6 stages of rapport. Always answer directly and tactically like Chase would in a training session. Give real scripts and examples. Never be vague."},
            {"role": "user", "content": question}
        ]
    )
    return jsonify({"answer": response.choices[0].message.content})

@app.route('/email', methods=['POST'])
def email():
    email_text = request.json.get('email')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Chase Hughes. Read this email and write a response using behavioral influence principles. Be strategic, direct, and use rapport building techniques."},
            {"role": "user", "content": f"Write a response to this email:\n\n{email_text}"}
        ]
    )
    return jsonify({"answer": response.choices[0].message.content})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
