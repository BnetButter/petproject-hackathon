from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys

URL = "https://aphis.file.force.com/sfc/dist/version/download/?oid=00Dt0000000GyZH&ids=0683d00000BAnTJ&d=%2Fa%2F3d000002BozY%2FYnbb.hjAOBnfnPlY2fZHniZk6qKJA8tdEQWNhxiAmAM&asPdf=false"
OUT = "."

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

# Create a new instance of the Chrome driver within the 'with' statement
with webdriver.Chrome(options=chrome_options) as driver:
    # Open the URL
    driver.get(URL)
    time.sleep(2)
    
