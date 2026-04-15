from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Simple keyword‑based answer function (replace with your LLM later)
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

# HTML with chat interface and pricing section
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Westside Dentistry AI</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f0f7ff; }
        .card { background: white; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 24px; overflow: hidden; }
        .card-header { background: #0078d4; color: white; padding: 16px 20px; font-size: 20px; font-weight: bold; }
        .card-body { padding: 20px; }
        .chat-messages { height: 400px; overflow-y: auto; padding: 16px; background: #fafafa; border-bottom: 1px solid #eee; }
        .message { margin-bottom: 16px; display: flex; }
        .user-message { justify-content: flex-end; }
        .bot-message { justify-content: flex-start; }
        .bubble { max-width: 70%; padding: 10px 16px; border-radius: 20px; }
        .user-bubble { background: #0078d4; color: white; }
        .bot-bubble { background: #e9ecef; color: #333; }
        .input-area { display: flex; padding: 16px; background: white; gap: 10px; }
        input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 24px; font-size: 16px; }
        button { background: #0078d4; color: white; border: none; padding: 12px 24px; border-radius: 24px; cursor: pointer; font-size: 16px; }
        button:hover { background: #005a9e; }
        .pricing-grid { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
        .pricing-card { flex: 1; min-width: 180px; background: #f8f9fa; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #e0e0e0; }
        .price { font-size: 28px; font-weight: bold; color: #0078d4; margin: 10px 0; }
        .contact-btn { background: #28a745; margin-top: 20px; display: inline-block; padding: 12px 30px; border-radius: 30px; color: white; text-decoration: none; }
        .contact-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-header">🦷 Westside Children's Dentistry AI Assistant</div>
        <div class="chat-messages" id="messages">
            <div class="message bot-message"><div class="bubble bot-bubble">Hello! Ask me about hours, services, insurance, or appointments.</div></div>
        </div>
        <div class="input-area">
            <input type="text" id="prompt" placeholder="Type your question here..." onkeypress="if(event.keyCode==13) sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <div class="card">
        <div class="card-header">💰 Pricing</div>
        <div class="card-body">
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Basic</h3>
                    <div class="price">$200<span style="font-size: 14px;">/month</span></div>
                    <p>Up to 500 questions/month<br>Email support<br>24/7 uptime</p>
                </div>
                <div class="pricing-card">
                    <h3>Pro</h3>
                    <div class="price">$500<span style="font-size: 14px;">/month</span></div>
                    <p>Up to 2,000 questions/month<br>Priority support<br>Custom answers</p>
                </div>
                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">Custom</div>
                    <p>Unlimited questions<br>Dedicated support<br>Full integration</p>
                </div>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <a href="mailto:ajkimx333@gmail.com?subject=Westside%20Dental%20AI%20Demo" class="contact-btn">📧 Contact for Demo</a>
            </div>
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