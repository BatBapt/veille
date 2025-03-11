import os
import arxiv
from mistralai import Mistral
from dotenv import load_dotenv
import tools as tools

load_dotenv()
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')


if __name__ == "__main__":

    client = arxiv.Client(num_retries=5)
    search = tools.make_query(query="cat:cs.AI AND submittedDate:[20250201 TO 20250301]", nb_result=10)
    tools.download_search(client=client, search=search, nb_result=10, output_path="pdfs")

    exit()

client = Mistral(api_key=MISTRAL_API_KEY)


uploaded_pdf = client.files.upload(
    file={
        "file_name": "01.pdf",
        "content": open("01.pdf", "rb"),
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




markdown_str = get_combined_markdown(ocr_response)

with open("01.md", "w", encoding="utf-8") as f:
    f.write(markdown_str)