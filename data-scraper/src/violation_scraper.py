from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

import zlib
import time
import json
from urllib.parse import parse_qs, urlencode
import random

from queue import Queue, Empty

import sys

OUTPUT_FILE=sys.argv[1]

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

# URL to open
url = "https://aphis.my.site.com/PublicSearchTool/s/inspection-reports"

INTERCEPT_URL = "https://aphis.my.site.com/PublicSearchTool/s/sfsites/aura"

queue = Queue()

dataframe_ptr = [None]

def response_interceptor(request, response):
    if request.method == 'POST' and  INTERCEPT_URL in request.url:  # Adjust URL accordingly
        # Modify the response if needed
        if response.status_code != 200:
            return

        if response.headers.get('Content-Encoding') != 'gzip':
            return
    
        decompressed_body = zlib.decompress(response.body, zlib.MAX_WBITS|16)
        asstr = decompressed_body.decode('utf-8', errors='replace')
        if "reportLink" not in asstr:
            return
        
        response_json = json.loads(decompressed_body.decode('utf-8', errors='replace'))
        actions = response_json["actions"]
        if len(actions) > 1:
            action = response_json["actions"][1]
        else:
            action = response_json["actions"][0]
        data = action["returnValue"]["results"]

        # Initiate dataframe
        if dataframe_ptr[0] is None:
            dataframe_ptr[0] = pd.DataFrame(data)
        else: 
            # Append to dataframe
            new_df = pd.DataFrame(data)
            dataframe_ptr[0] = pd.concat([dataframe_ptr[0], new_df], ignore_index=True)

        print(dataframe_ptr[0])

        queue.put("NEXT")
        
# Create a new instance of the Chrome driver within the 'with' statement
with webdriver.Chrome(options=chrome_options) as driver:
    driver.response_interceptor = response_interceptor
    # Open the URL
    driver.get(url)
    
    time.sleep(3)

    # Example: Find a specific element and print its text
    # Adjust the selectors based on the actual elements you want to scrape
    select_element = driver.find_elements(By.TAG_NAME, "select")[1]  # Example selector
    select = Select(select_element)
    select.select_by_visible_text("MISSOURI (MO)")
    
    inspection = driver.find_element(By.XPATH, "//a[contains(text(), 'View Inspection Reports')]")
    inspection.click()

    time.sleep(3)

    select_element = driver.find_elements(By.TAG_NAME, "select")[3]  # Example selector
    select = Select(select_element)

    
    select.select_by_visible_text("DOGS")

    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    search_button.click()
    
    while True:
        try:
            queue.get(timeout=20)
        except Empty:
            df = dataframe_ptr[0]
           
            df.to_csv(OUTPUT_FILE)

            exit()
            
        time.sleep(1)
        button = driver.find_elements(By.XPATH, '//button[text()=">"]')[2]    
        button.click()


