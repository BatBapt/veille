from mistralai import Mistral
from dotenv import load_dotenv
import tools as tools
import os

load_dotenv()
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY') # wWjwniwVkvvYlVT2aVf3CSqbSMzMvohe


def extract_content(inputs_path, outputs_path):
    if not os.path.exists(outputs_path): os.mkdir(outputs_path)

    for file in os.listdir(inputs_path):
        output_filename = file.split(".")[0] + ".md"
        output_filename = os.path.join(outputs_path, output_filename)
        if os.path.exists(output_filename):
            continue

        print(f"Processing OCR for {file}...")
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.join(inputs_path, file),
                "content": open(os.path.join(inputs_path, file), "rb"),
            },
            purpose="ocr"
        )

        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            },
            include_image_base64=True
        )

        markdown_str = tools.get_combined_markdown(ocr_response)

        with open(output_filename, "w", encoding="utf-8") as f:
            # f.write(markdown_str)
            for page in ocr_response.pages:
                f.write(page.markdown)
                f.write("\n\n")
        break


def summarize(inputs_path, outputs_path):
    if not os.path.exists(outputs_path): os.mkdir(outputs_path)

    for file in os.listdir(inputs_path):
        output_filename = file.split(".")[0] + ".txt"
        output_filename = os.path.join(outputs_path, output_filename)

        if os.path.exists(output_filename):
            continue

        print(f"Processing summerization for {file}...")
        input_file = os.path.join(inputs_path, file)

        with open(input_file, "r", encoding="utf-8") as f:
            document_content = f.read()

        chat_response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "assistant",
                    "content": "Tu es un super assistant qui aide les chercheurs à faire de la veille."
                               "Tes réponses doivent être claire et compréhensible, tu dois résumer les documents en français.",
                },
                {
                    "role": "user",
                    "content": document_content
                }
            ]
        )

        print(chat_response.choices[0].message.content)
        break



if __name__ == "__main__":
    client = Mistral(api_key=MISTRAL_API_KEY)

    inputs_path = "pdfs"
    outputs_md_path = "mds"
    output_txt_path = "resums"

    extract_content(inputs_path=inputs_path, outputs_path=outputs_md_path)
    summarize(inputs_path=outputs_md_path, outputs_path=output_txt_path)



