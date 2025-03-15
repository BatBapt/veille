import os
import arxiv
import time


def make_query(query, nb_result):
    search = arxiv.Search(
        query=query,
        max_results=nb_result,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    return search


def download_search(client, search, nb_result, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i, elem in enumerate(client.results(search)):
        output_file = f"{elem.title}.pdf"
        if "/" in output_file:
            output_file = output_file.replace("/", "_")

        tmp_full_output_path = os.path.join(output_path, output_file)
        if os.path.exists(tmp_full_output_path):
            print(f"{output_file} already exists!")
            continue

        elem.download_pdf(dirpath=output_path, filename=output_file)

        if os.path.getsize(tmp_full_output_path) == 0:
            os.remove(tmp_full_output_path)
            print(f"{output_file} has been deleted!")

        print(f"{i + 1}/{nb_result}")
        time.sleep(2)


def assert_download(path, ext_looking="pdf"):
    for file in os.listdir(path):
        if not file.endswith(ext_looking):
            print(f"{file} is not a {ext_looking.upper()} file!")
            os.remove(os.path.join(path, file))



def replace_images_in_markdown(markdown_str, images_dict):
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})")
    return markdown_str


def get_combined_markdown(ocr_response):
    markdowns = []
    for page in ocr_response.pages:
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))

    return "\n\n".join(markdowns)