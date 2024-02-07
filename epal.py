from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

vorur = []
name_counts = {}
ur = [
    "https://www.epal.is/vorur/epal-klassik/",
    "https://www.epal.is/vorur/husgogn/",
    "https://www.epal.is/vorur/gjafahugmyndir/",
    "https://www.epal.is/vorur/islensk-honnun/",
    "https://www.epal.is/vorumerki/hay/",
    "https://www.epal.is/vorur/herbergi/svefnherbergi/",
    "https://www.epal.is/string-samsetningar/",
    "https://www.epal.is/vorur/lampar/",
    "https://www.epal.is/vorur/barnavorur/",
    "https://www.epal.is/vorur/herbergi/stofa/",
    "https://www.epal.is/vorur/lifstilsvorur/ferdalog-utivist/",
    "https://www.epal.is/vorur/lifstilsvorur/saelgaeti-lifstilsvorur/#:~:text=Sykurlaust-,Sælkeri,-Drykkjarföng",
    "https://www.epal.is/vorur/bordbunadur/",
    "https://www.epal.is/vorur/herbergi/eldhus-herbergi/",
    "https://www.epal.is/vorur/lifstilsvorur/kerti-ilmstangir/",
    "https://www.epal.is/vorur/herbergi/badherbergi-herbergi/"
]

new_urls = []
for base_url in ur:
    new_urls.extend([f"{base_url}page/{i}/" for i in range(2, 50)])

urls = ur + new_urls
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# <p class="item-cate-title category uppercase is-smaller no-text-overflow product-cat op-7"> Cane-line </p>

for url in urls:
    try:
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="box-text box-text-products")

        for row in data:
            nafn = row.find('p', class_='item-cate-title category uppercase is-smaller no-text-overflow product-cat op-7')
            nafn2 = row.find("a", class_= "")
            nafn = nafn.text.strip() + " " + nafn2.text.strip()
            bdi_elements = row.find_all("bdi")
            
            if (len(bdi_elements) == 2):
                sale = True
                sale_price = bdi_elements[0].text.strip().replace("\xa0kr", "")
                regular_price = bdi_elements[1].text.strip().replace("\xa0kr", "")
                if(sale_price > regular_price):
                    temp = regular_price
                    regular_price = sale_price
                    sale_price = temp
            else:
                sale = False
                regular_price_element = bdi_elements[0]
                regular_price = regular_price_element.text.strip() if regular_price_element else None
                sale_price = None

            if nafn and (sale_price or regular_price):
                temp = {
                    "Nafn": nafn,
                    "Verð": regular_price,
                    "Útsöluverð": sale_price,
                    "On_sale": sale
                }
                print(temp)
                vorur.append(temp)
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
print(vorur)
