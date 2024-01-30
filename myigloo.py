from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

vorur = {}
urls = ["https://myigloo.is/listings"]

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content")))

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # Wait to load page
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find_all("div", class_="content")
        for row in data:
            price = row.find('p', class_='small-section-title mb-0 listing-price')
            nafn = row.find("p", class_="igloo-text small listing-location mb-0")

            if nafn and price:
                vorur[nafn.text.strip()] = price.text.strip()
                print(nafn.text.strip(), price.text.strip())

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
