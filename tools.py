import os
import arxiv


def make_query(query, nb_result):
    search = arxiv.Search(
        query=query,
        max_results=nb_result,
        sort_order=arxiv.SortOrder.Ascending,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    return search


def download_search(client, search, nb_result, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i, elem in enumerate(client.results(search)):
        elem.download_pdf(dirpath=output_path, filename=f"{elem.title}.pdf")
        print(f"{i+1}/{nb_result}")

    for file in os.listdir(output_path):
        if not file.endswith(".pdf"):
            print(f"{file} bugged ?")
            os.remove(os.path.join(output_path, file))



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