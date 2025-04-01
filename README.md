# About Veille

This github project is about IT monitoring.\
This assistant will fetch, extract and summerize the papers that are just published on the Arxiv plateform.

The process is simple:
- The fetch_doc.py file wile fetch the paper and download the PDF files.
- The ocr.py file will extract the content of the PDF using into a Mardown format using Mistral API. 
- The same mardown files will be summerize (also using Mistral API) and store them as text files.
- The api.py file will run a Flask server and display the content the AI resumed (and more)

And now you have 2 options

## How to install & run ?

- Clone this repository.
- Go the configurations.py file and see if you want to update the paths for the scripts
- Create a new '.env' file and paste create a new line: 'MISTRAL_API_KEY=api_key' (see documentation)
- Update (or not) the query in the fetch_doc.py file then run it
- Also run ocr.py file

### For the web server

- And finally run api.py

### To email your device

First you need to create a rule in your server (basically your own device for the test, or a remote one) to allow incoming connection for the port 8000.\

Then you need to open a cmd shell and type the command `python -m http.server 8000` (in admin/sudo mode)

Now in the .env file you need to create news variable:
  - MAIL_USERNAME=your_email_address
  - MAIL_PASSWORD=your_account_password, with Gmail you will need to create an application password, see their document (take 5min to do it)
  - REMOTE_PDF_PATH=the_pdf_where_your_pdfs_are
  - MY_IP_PORT=the_public_ip_of_your_server:port, exemple: 192.168.1.154:8000 (the port should be the same as the option given before)
- And finally you can run mail.py

**I'm looking for an easier method**


## Futur & Todo

- [ ] Update the code in a more scalabe way
- [ ] Some PDF files may download incorrectly
- [ ] Configure a cron job for the script 
  - [ ] fetch the doc, for instance, 1 time a week
  - [ ] Automatise the whole processus of fetching and storing
- [x] Set up a mail environnement with/without the Flask Server 
  - [x] Displaying webpage
  - [x] Sending mail
  - [x] Download PDF on your device
- [ ] Add more sources for the paper ?





