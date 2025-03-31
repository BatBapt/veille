# About Veille

This github project is about IT monitoring.\
This assistant will fetch, extract and summerize the papers that are just published on the Arxiv plateform.

The process is simple:
- The fetch_doc.py file wile fetch the paper and download the PDF files.
- The ocr.py file will extract the content of the PDF using into a Mardown format using Mistral API. 
- The same mardown files will be summerize (also using Mistral API) and store them as text files.
- The api.py file will run a Flask server and display the content the AI resumed (and more)

## How to install & run ?

- Clone this repository.
- Go the configurations.py file and see if you want to update the paths for the scripts
- Create a new '.env' file and paste create a new line: 'MISTRAL_API_KEY=api_key' (see documentation)
- Update (or not) the query in the fetch_doc.py file then run it
- Also run ocr.py file
- And finally run api.py

## Futur & Todo

- [ ] Update the code in a more scalabe way
- [ ] Some PDF files may download incorrectly
- [ ] Configure a cron job for the script 
- [ ] Set up a mail environnement with/without the Flask Server 
- [ ] Add more sources for the paper ?




