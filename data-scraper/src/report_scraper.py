from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import glob
import os
import fitz  # PyMuPDF
import pandas as pd


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""

    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    return text

OUT, input_csv, output_csv = sys.argv[1:]

input_dataframe = pd.read_csv(input_csv)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

chrome_options.add_experimental_option("prefs", {
    "download.default_directory": OUT,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

new_rows = []
# Create a new instance of the Chrome driver within the 'with' statement
with webdriver.Chrome(options=chrome_options) as driver:
    # Open the URL

    for i, row in input_dataframe.iterrows():
        URL = row["reportLink"]
        ID = row["id"]
        driver.get(URL)
        time.sleep(5)


        pdf_files = glob.glob(os.path.join(OUT, '*.pdf'))
        if not pdf_files:
            new_rows.append({ "id": ID, text: None })
            continue

        assert len(pdf_files) == 1
        file = pdf_files[0]

        text = extract_text_from_pdf(file)
        print(text)

        os.remove(file)

        new_rows.append({
            "id": ID,
            "text": text
        })

df = pd.DataFrame(new_rows)
print(df)
df.to_csv(output_csv, index=False)


    


    
