from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
from pinecone import Pinecone
import os

app = Flask(*name*)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("chase-hughes")

def search_knowledge(question, top_k=5):
try:
response = client.embeddings.create(
input=question,
model="text-embedding-3-small"
)
query_vector = response.data[0].embedding
results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
chunks = [match["metadata"]["text"] for match in results["matches"] if "text" in match["metadata"]]
return "\n\n".join(chunks)
except Exception as e:
print(f"Pinecone search error: {e}")
return ""

HTML = """

<!DOCTYPE html>

<html>
<head>
    <title>Chase Hughes AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #0a0a0a; color: #ffffff; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px 20px; text-align: center; border-bottom: 2px solid #e94560; box-shadow: 0 4px 20px rgba(233,69,96,0.3); }
        .header h1 { font-size: 2.5em; color: #e94560; letter-spacing: 2px; text-transform: uppercase; }
        .header p { color: #888; margin-top: 8px; font-size: 0.9em; letter-spacing: 1px; }
        .container { max-width: 850px; margin: 0 auto; padding: 30px 20px; }
        .tab { display: flex; background: #111; border-radius: 10px; padding: 5px; margin-bottom: 25px; border: 1px solid #222; }
        .tab button { flex: 1; background: none; border: none; color: #888; padding: 12px 20px; cursor: pointer; font-size: 15px; border-radius: 8px; transition: all 0.3s; font-weight: 500; }
        .tab button.active { background: #e94560; color: white; box-shadow: 0 4px 15px rgba(233,69,96,0.4); }
        .tab button:hover:not(.active) { color: #e94560; background: #1a1a1a; }
        .tabcontent { display: none; }
        .tabcontent.active { display: block; }
        .card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 25px; }
        .card h2 { color: #e94560; margin-bottom: 15px; font-size: 1.3em; letter-spacing: 1px; }
        textarea { width: 100%; padding: 15px; background: #0a0a0a; color: #ffffff; border: 1px solid #333; border-radius: 8px; font-size: 14px; line-height: 1.6; resize: vertical; font-family: 'Segoe UI', Arial, sans-serif; }
        textarea:focus { outline: none; border-color: #e94560; }
        button.submit { background: linear-gradient(135deg, #e94560, #c23152); color: white; border: none; padding: 14px 35px; border-radius: 8px; cursor: pointer; font-size: 15px; margin-top: 15px; font-weight: 600; letter-spacing: 1px; }
        .response { background: #0a0a0a; border: 1px solid #333; border-left: 4px solid #e94560; padding: 20px; border-radius: 8px; margin-top: 20px; white-space: pre-wrap; line-height: 1.8; font-size: 14px; }
        .footer { text-align: center; padding: 20px; color: #444; font-size: 12px; border-top: 1px solid #1a1a1a; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Chase Hughes AI</h1>
        <p>Behavioral Intelligence - Powered by Chase Hughes Complete Library</p>
    </div>
    <div class="container">
        <div class="tab">
            <button class="active" onclick="openTab('chat', this)">Chat</button>
            <button onclick="openTab('email', this)">Email Assistant</button>
            <button onclick="openTab('situation', this)">Situation Advisor</button>
        </div>
        <div id="chat" class="tabcontent active">
            <div class="card">
                <h2>Ask Chase Hughes</h2>
                <textarea id="question" rows="4" placeholder="Ask anything about behavior, influence, or psychology..."></textarea>
                <br>
                <button class="submit" onclick="askChase()">Get Answer</button>
                <div id="chat-response" class="response" style="display:none"></div>
            </div>
        </div>
        <div id="email" class="tabcontent">
            <div class="card">
                <h2>Email Assistant</h2>
                <textarea id="email-input" rows="8" placeholder="Paste the email you received..."></textarea>
                <br>
                <button class="submit" onclick="writeEmail()">Write Response</button>
                <div id="email-response" class="response" style="display:none"></div>
            </div>
        </div>
        <div id="situation" class="tabcontent">
            <div class="card">
                <h2>Situation Advisor</h2>
                <textarea id="situation-input" rows="8" placeholder="Describe any social situation..."></textarea>
                <br>
                <button class="submit" onclick="adviseSituation()">Get Chase's Approach</button>
                <div id="situation-response" class="response" style="display:none"></div>
            </div>
        </div>
        <script>
            function openTab(name, btn) {
                document.querySelectorAll('.tabcontent').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab button').forEach(b => b.classList.remove('active'));
                document.getElementById(name).classList.add('active');
                btn.classList.add('active');
            }
            async function askChase() {
                const q = document.getElementById('question').value;
                const r = document.getElementById('chat-response');
                r.style.display = 'block';
                r.innerHTML = 'Thinking...';
                const res = await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question:q})});
                const data = await res.json();
                r.innerHTML = data.answer;
            }
            async function writeEmail() {
                const e = document.getElementById('email-input').value;
                const r = document.getElementById('email-response');
                r.style.display = 'block';
                r.innerHTML = 'Crafting response...';
                const res = await fetch('/email', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email:e})});
                const data = await res.json();
                r.innerHTML = data.answer;
            }
            async function adviseSituation() {
                const s = document.getElementById('situation-input').value;
                const r = document.getElementById('situation-response');
                r.style.display = 'block';
                r.innerHTML = 'Analyzing situation...';
                const res = await fetch('/situation', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({situation:s})});
                const data = await res.json();
                r.innerHTML = data.answer;
            }
        </script>
    </div>
    <div class="footer">
        Built on Chase Hughes complete library - The Ellipsis Manual - Six Minute X-Ray - Behavior Ops Manual - Tongue
    </div>
</body>
</html>
"""

@app.route('/')
def home():
return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
question = request.json.get('question')
knowledge = search_knowledge(question)
system_prompt = "You are Chase Hughes, behavioral expert and author of The Ellipsis Manual, Six Minute X-Ray, Tongue, and The Behavior Ops Manual. You know these frameworks deeply: FATE Model (Focus = brain automatically focuses on novelty and pattern interruption, Authority = establish credibility and perceived power, Tribe = humans need belonging, Emotion = emotion drives all decisions). BMEPA. Elicitation - getting information without direct questioning using bracketing, presumptive attribution, word echoing. Behavior stacking. Baseline - establishing normal behavior to detect deviations. Compliance triggers - reciprocity, social proof, authority, scarcity. Cold read. Rapport architecture. Always answer directly and tactically like Chase would in a training session. Give real scripts and examples. Never be vague."
if knowledge:
system_prompt += f"\n\nHere is relevant content from Chase Hughes materials:\n{knowledge}"
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": question}
]
)
return jsonify({"answer": response.choices[0].message.content})

@app.route('/email', methods=['POST'])
def email():
email_text = request.json.get('email')
knowledge = search_knowledge(email_text)
system_prompt = "You are Chase Hughes. Read this email and write a strategic response using behavioral influence principles including rapport building, compliance triggers, and elicitation techniques. Be direct and tactical."
if knowledge:
system_prompt += f"\n\nRelevant Chase Hughes content:\n{knowledge}"
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": "Write a response to this email:\n\n" + email_text}
]
)
return jsonify({"answer": response.choices[0].message.content})

@app.route('/situation', methods=['POST'])
def situation():
situation_text = request.json.get('situation')
knowledge = search_knowledge(situation_text)
system_prompt = "You are Chase Hughes. Analyze this social situation and give a precise tactical approach. Include: 1) What is actually happening behaviorally 2) The exact approach Chase would take 3) Word for word scripts to use 4) What to watch for in their response. Be direct and specific."
if knowledge:
system_prompt += f"\n\nRelevant Chase Hughes content:\n{knowledge}"
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": "Advise me on this situation:\n\n" + situation_text}
]
)
return jsonify({"answer": response.choices[0].message.content})

if *name* == '*main*':
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
