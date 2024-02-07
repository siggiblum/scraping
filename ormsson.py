from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#Allt virðist virka vel fyrir afslætti og venjulegar vörur

vorur = []
ur = [
    "https://ormsson.is/products/hljod-og-mynd", 
    "https://ormsson.is/products/heimilistaeki",
    "https://ormsson.is/products/leikjatolvur-og-afthreying",
    "https://ormsson.is/products/busahold-1" 
]
urls = []
for base_url in ur:
    urls.extend([f"{base_url}#page={i}" for i in range(2, 50)])

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
for url in urls:
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="productItem")
        for row in data:
            div = row.find("div", class_="header text-semi pl-3 pr-3")
            nafn = div.find('a', class_='') if div else None            
            regular_price_element = row.find("span", class_="oldPrice")

            if (regular_price_element):
                sale = True
                regular_price = regular_price_element.text.strip()
                sale_price_element = row.find("span", class_="price")
                sale_price = sale_price_element.text.strip() if sale_price_element else None
            else:
                sale = False
                regular_price_element = row.find("span", class_="price")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
                sale_price = None

            if nafn and (sale_price or regular_price):
                temp = {
                    "Nafn": nafn.text.strip(),
                    "Verð": regular_price,
                    "Útsöluverð": sale_price,
                    "On_sale": sale
                }
                print(temp)
                vorur.append(temp)
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
