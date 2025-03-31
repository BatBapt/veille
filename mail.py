from flask import Flask, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration de l'email
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("GMAIL_USERNAME")
SMTP_PASSWORD = os.getenv("GMAIL_PASSWORD")

@app.route('/')
def send_email():
    to_email = SMTP_USERNAME  # mail to yourself
    subject = "Hello"
    body = "Coucou"

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    pdf_path = "pdfs/Compositional Subspace Representation Fine-tuning for Adaptive Large Language Models.pdf"
    try:
        attachment = open(pdf_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
        msg.attach(part)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    try:
        # Connexion au serveur SMTP et envoi de l'email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)