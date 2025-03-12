import arxiv
import tools as tools


if __name__ == "__main__":
    client = arxiv.Client(num_retries=5)
    search = tools.make_query(query="cat:cs.AI AND submittedDate:[20250201 TO 20250301]", nb_result=10)
    tools.download_search(client=client, search=search, nb_result=10, output_path="pdfs")


