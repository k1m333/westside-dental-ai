from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Westside Dentistry AI</title>
    <style>
        body {{ font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }}
        .response {{ margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Westside Children's Dentistry AI Assistant</h1>
    <form method="post">
        <input type="text" name="prompt" placeholder="Ask about hours, services, insurance..." style="width: 70%; padding: 8px;">
        <button type="submit" style="padding: 8px 16px;">Ask</button>
    </form>
    <div class="response">{response}</div>
</body>
</html>
"""

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

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTML_FORM.format(response="")

@app.post("/", response_class=HTMLResponse)
async def post_form(prompt: str = Form(...)):
    response = answer_question(prompt)
    return HTML_FORM.format(response=f'<div class="response">{response}</div>')