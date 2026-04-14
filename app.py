from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Simple keyword‑based answer function
def answer_question(query: str) -> str:
    q = query.lower()
    if 'hour' in q or 'when' in q or 'open' in q:
        return "Our office hours are: Monday 7:30am to 2:00pm, Tuesday closed, Wednesday 7:30am to 2:00pm, Thursday 7:30am to 2:00pm, Friday 7:30am to 2:00pm. Closed weekends."
    elif 'insurance' in q or 'cover' in q or 'payment' in q:
        return "We accept most major credit cards and insurance plans. Our staff can help with insurance claims. Please call the office for specific questions."
    elif 'service' in q or 'procedure' in q or 'offer' in q:
        return "We offer dental exams and cleanings, preventive care, sealants, fluoride, mouthguards, pediatric dentistry, special needs dentistry, and emergency dental care."
    elif 'appointment' in q or 'book' in q or 'schedule' in q:
        return "To book an appointment, please call our office during business hours. We don't have online booking yet."
    else:
        return "I'm not sure about that. Please call our office for more information."

# HTML with chat interface (no separate /ask endpoint)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Westside Dentistry AI</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .chat-container { background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
        .chat-header { background: #0078d4; color: white; padding: 15px; font-size: 18px; }
        .chat-messages { height: 400px; overflow-y: auto; padding: 15px; background: #fafafa; }
        .message { margin-bottom: 15px; display: flex; }
        .user-message { justify-content: flex-end; }
        .bot-message { justify-content: flex-start; }
        .bubble { max-width: 70%; padding: 10px 15px; border-radius: 18px; }
        .user-bubble { background: #0078d4; color: white; }
        .bot-bubble { background: #e9ecef; color: #333; }
        .input-area { display: flex; padding: 15px; background: white; border-top: 1px solid #ddd; }
        input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 20px; margin-right: 10px; }
        button { background: #0078d4; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; }
        button:hover { background: #005a9e; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">🤖 Westside Children's Dentistry AI Assistant</div>
        <div class="chat-messages" id="messages">
            <div class="message bot-message"><div class="bubble bot-bubble">Hello! Ask me about hours, services, or insurance.</div></div>
        </div>
        <div class="input-area">
            <input type="text" id="prompt" placeholder="Type your question here..." onkeypress="if(event.keyCode==13) sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('prompt');
            const prompt = input.value.trim();
            if (!prompt) return;
            
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML += `<div class="message user-message"><div class="bubble user-bubble">${escapeHtml(prompt)}</div></div>`;
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            const formData = new FormData();
            formData.append('prompt', prompt);
            const response = await fetch('/', { method: 'POST', body: formData });
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const responseText = doc.querySelector('.response')?.innerText || 'Error. Please try again.';
            messagesDiv.innerHTML += `<div class="message bot-message"><div class="bubble bot-bubble">${escapeHtml(responseText)}</div></div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTML_PAGE

@app.post("/", response_class=HTMLResponse)
async def post_form(prompt: str = Form(...)):
    response = answer_question(prompt)
    return f'<div class="response">{response}</div>'