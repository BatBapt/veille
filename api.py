import os
import re
from flask import Flask, render_template, send_from_directory
import configuration as cfg
import sqlite3


app = Flask(__name__)

inputs_path = cfg.RESUME_PATH
pdfs_path = cfg.PDF_PATH


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

    print(parsed_data["key_points"])
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

@app.route("/")
def display_papers():
    paper_data = []
    for paper in os.listdir(inputs_path):
        paper_path = os.path.join(inputs_path, paper)

        pdf_path = os.path.join(pdfs_path, paper.replace(".txt", ".pdf"))

        with open(paper_path, "r", encoding="utf-8") as f:
            document = f.read()

        parsed_doc = parse_document(document.strip())
        parsed_doc["pdf_link"] = pdf_path
        parsed_doc["pdf_name"] = paper.replace(".txt", ".pdf")
        paper_data.append(parsed_doc)

    return render_template("index.html", papers=paper_data)

@app.route('/pdfs/<path:filename>')
def download_file(filename):
    return send_from_directory(pdfs_path, filename, as_attachment=True)


if __name__ == '__main__':
    # display_papers()
    app.run(debug=True)