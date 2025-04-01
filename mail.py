import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import re
from dotenv import load_dotenv
from jinja2 import Template
from premailer import transform
import configuration as cfg

load_dotenv()

# Configuration du script
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("MAIL_USERNAME")
SMTP_PASSWORD = os.getenv("MAIL_PASSWORD")
REMOTE_PDF_PATH = os.getenv("REMOTE_PDF_PATH")
MY_IP_PORT = os.getenv("MY_IP_PORT")

RESUME_PATH = cfg.RESUME_PATH
PDFS_PATH = f"http://{MY_IP_PORT}/{REMOTE_PDF_PATH}"

def parse_document(text):
    parsed_data = {}

    # Extraction du nom
    name_match = re.search(r'\*\*NOM\*\*: (.+)', text)
    key = "name"
    name_value = name_match.group(1) if name_match else None
    parsed_data[key] = name_value

    # Extraction des auteurs
    authors_match = re.search(r'\*\*AUTEURS\*\*: (.+)', text)
    key = "authors"
    parsed_data[key] = authors_match.group(1) if authors_match else None

    # Extraction des points clés (optionnel, avec variantes d'orthographe)
    key_points_match = re.search(r'\*\*(POINTS CL[ÉE]S)\*\*:(.+?)(\*\*R[ÉE]SUM[ÉE]\*\*|$)', text, re.DOTALL)
    if key_points_match:
        points = re.findall(r'\d+\.\s*(.+)', key_points_match.group(2))
        key = "key_points"
        parsed_data[key] = [point.strip() for point in points] if points else None
        if parsed_data[key] is None:
            parsed_data[key] = {f"Error with document {name_value}": "Something went wrong with this document during the parsing process"}

    # Extraction du résumé (optionnel, avec variantes d'orthographe)
    summary_match = re.search(r'\*\*R[ÉE]SUM[ÉE]\*\*:(.+?)(\*\*LINKS\*\*|$)', text, re.DOTALL)
    key = "resum"
    parsed_data[key] = summary_match.group(1).strip() if summary_match else None

    # Extraction des liens
    links_match = re.search(r'\*\*LINKS\*\*:\s*(.+)', text, re.DOTALL)
    if links_match:
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', links_match.group(1))
        key = "links"
        parsed_data[key] = {title: url for title, url in links} if links else None
        if parsed_data[key] is None:
            parsed_data[key] = {f"Error with document {name_value}": "Something went wrong with this document during the parsing process"}

    return parsed_data

def get_papers():
    paper_data = []
    for paper in os.listdir(RESUME_PATH):
        paper_path = os.path.join(RESUME_PATH, paper)

        with open(paper_path, "r", encoding="utf-8") as f:
            document = f.read()

        parsed_doc = parse_document(document.strip())
        parsed_doc["pdf_link"] = os.path.join(PDFS_PATH, paper.replace(".txt", ".pdf"))
        parsed_doc["pdf_name"] = paper.replace(".txt", ".pdf")
        paper_data.append(parsed_doc)

    return paper_data

def send_email():
    to_email = SMTP_USERNAME  # mail to yourself
    subject = "Hello"

    with open("templates/mail.html", "r", encoding="utf-8") as template:
        html_content = template.read()

    with open("static/mail.css", "r", encoding="utf-8") as css:
        css_content = css.read()

    html_content = html_content.replace('</head>', f'<style>{css_content}</style></head>')

    papers = get_papers()

    template = Template(html_content)
    html_content_rendered = template.render(papers=papers)

    html_content_rendered = transform(html_content_rendered)

    print(html_content_rendered)

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content_rendered, 'html'))

    pdf_path = "pdfs/Compositional Subspace Representation Fine-tuning for Adaptive Large Language Models.pdf"
    try:
        attachment = open(pdf_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
        msg.attach(part)
    except Exception as e:
        print(e)
        return False

    try:
        # Connexion au serveur SMTP et envoi de l'email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    sent = send_email()
    if sent:
        print("OK")
    else:
        print("PAS OK")