from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

vorur = {}
urls = ["https://www.jens.is/collections/skartgripir"]
for i in range(2, 80):
    urls.append(f"{urls[0]}?page={i}")

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-product__meta")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find_all("div", class_="grid-product__meta")
        for row in data:
            nafn = row.find('div', class_='grid-product__title')
            price = row.find("span", class_="money")

            if nafn and price:
                vorur[nafn.text.strip()] = price.text.strip()
        print(vorur)

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
