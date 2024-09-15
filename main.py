import markdown
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

from gemini import gemini

load_dotenv()

app = FastAPI()

class InputData(BaseModel):
    idea: str
    email: EmailStr

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)

@app.post("/submit")
async def submit_idea(data: InputData):
    # Send test email
    send_email(data.email, data.idea)
    return {"message": "Idea submitted and test email sent successfully"}

def send_email(to_email: str, idea: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Test Email - Your Idea Submission"

    prompt = (
        'You are startup founder who want to hire a designer to build you a landing page. '
        'Write a detailed spec for the designer based on the following business idea. '
        f'IDEA: {idea}'
    )
    response = gemini(prompt)

    # Convert Markdown to HTML
    body = markdown.markdown(response)
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.send_message(message)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)