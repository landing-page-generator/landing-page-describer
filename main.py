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
    productName: str
    idealCustomer: str
    jobToBeDone: str
    howYouHelp: str
    email: EmailStr

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content)

@app.post("/submit")
async def submit_idea(data: InputData):
    # Send email
    send_email(data.email, data.productName, data.idealCustomer, data.jobToBeDone, data.howYouHelp)
    return {"message": "Answers submitted and email sent successfully"}

def send_email(to_email: str, product_name: str, ideal_customer: str, job_to_be_done: str, how_you_help: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = f"Landing Page Design Spec for {product_name}"

    prompt = (
        'You are startup founder who wants to hire a designer to build you a landing page. '
        'Write a detailed spec for the designer based on the following information:\n\n'
        f'Product/Service Name: {product_name}\n'
        f'Ideal Customer: {ideal_customer}\n'
        f'Job to be Done: {job_to_be_done}\n'
        f'How You Help: {how_you_help}\n\n'
        'Please provide a comprehensive design specification for the landing page, '
        'including suggested layout, key elements, color scheme, and any other relevant details.'
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