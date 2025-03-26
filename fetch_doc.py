import arxiv
import tools as tools
import datetime
import configuration as cfg


if __name__ == "__main__":
    date = datetime.date.today()
    date_delta = datetime.timedelta(days=30)
    date_ago = (date - date_delta).strftime("%Y%m%d")
    date_from = date.strftime("%Y%m%d")

    nb_result = 50

    client = arxiv.Client(delay_seconds=5, num_retries=3)
    search = tools.make_query(query=f"cat:cs.AI AND submittedDate:[{date_ago} TO {date_from}]", nb_result=nb_result)
    tools.download_search(client=client, search=search, nb_result=nb_result, output_path=cfg.PDF_PATH)
    tools.assert_download(path=cfg.PDF_PATH, ext_looking="pdf")
