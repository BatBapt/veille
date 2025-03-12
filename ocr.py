from mistralai import Mistral
from dotenv import load_dotenv
import tools as tools
import os

load_dotenv()
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY') # wWjwniwVkvvYlVT2aVf3CSqbSMzMvohe


if __name__ == "__main__":
    client = Mistral(api_key=MISTRAL_API_KEY)
    inputs_path = "pdfs/"
    outputs_path = "mds/"

    if not os.path.exists(outputs_path): os.mkdir(outputs_path)

    for file in os.listdir(inputs_path):
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

        # markdown_str = tools.get_combined_markdown(ocr_response)

        output_filename = file.split(".")[0] + ".md"
        with open(os.path.join(outputs_path, output_filename), "w", encoding="utf-8") as f:
            for page in ocr_response.pages:
                f.write(page.markdown)
                f.write("\n\n")

        print("Fin ocr")
        break

    print("début summerize")
    with open(os.path.join(outputs_path, output_filename), "r", encoding="utf-8") as f:
        document_content = f.read()

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "assistant",
                "content": "Tu es un super assistant qui aide les chercheurs à faire de la veille. "
                           "Tes réponses doivent être claire et concises, tu dois résumer les documents.",
            },
            {
                "role": "user",
                "content": document_content
            }
        ]
    )

    print(chat_response.choices[0].message.content)