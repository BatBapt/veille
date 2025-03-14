import os
import re
from flask import Flask, render_template
import configuration as cfg


app = Flask(__name__)


def parse_document(text):
    parsed_data = {}

    # Extraction du nom
    name_match = re.search(r'\*\*NOM\*\*: (.+)', text)
    key = "Nom"
    parsed_data[key] = name_match.group(1) if name_match else None

    # Extraction des auteurs
    authors_match = re.search(r'\*\*AUTEURS\*\*: (.+)', text)
    key = "Auteurs"
    parsed_data[key] = authors_match.group(1) if authors_match else None

    # Extraction des points clés (optionnel, avec variantes d'orthographe)
    key_points_match = re.search(r'\*\*(POINTS CL[ÉE]S)\*\*:(.+?)(\*\*R[ÉE]SUM[ÉE]\*\*|$)', text, re.DOTALL)
    if key_points_match:
        points = re.findall(r'\d+\. \*\*(.*?)\*\*: (.+)', key_points_match.group(2))
        key = "Points clés"
        parsed_data[key] = {title: desc for title, desc in points} if points else None

    # Extraction du résumé (optionnel, avec variantes d'orthographe)
    summary_match = re.search(r'\*\*R[ÉE]SUM[ÉE]\*\*:(.+)', text, re.DOTALL)
    key = "Résumé"
    parsed_data[key] = summary_match.group(1).strip() if summary_match else None

    return parsed_data

@app.route("/")
def display_papers():
    inputs_path = "resums/"
    pdfs_path = cfg.PDF_PATH
    paper_data = []
    for paper in os.listdir(inputs_path):
        paper_path = os.path.join(inputs_path, paper)

        pdf_path = os.path.join(pdfs_path, paper.replace(".txt", ".pdf"))

        with open(paper_path, "r", encoding="utf-8") as f:
            document = f.read()

        parsed_doc = parse_document(document.strip())
        parsed_doc["pdf_link"] = pdf_path
        paper_data.append(parsed_doc)

    return render_template("index.html", papers=paper_data)


if __name__ == '__main__':
    # display_papers()
    app.run(debug=True)