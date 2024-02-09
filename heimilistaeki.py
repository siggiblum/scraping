from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

vorur = []
url = ["https://ht.is/sjonvorp-og-spilarar.html", "https://ht.is/heimilistaeki.html", 
        "https://ht.is/litil-heimilistaeki.html", "https://ht.is/raftaeki.html",
        "https://ht.is/heilsu-og-snyrtitaeki.html", "https://ht.is/heilsu-og-snyrtitaeki.html",
        "https://ht.is/busahold.html", "https://ht.is/hljomtaeki.html", 
        "https://ht.is/snjallvorur.html", "https://ht.is/grill-og-gar-vorur.html",
        "https://ht.is/lysing.html", "https://ht.is/b-vorur.html"]

urls = []
for base_url in url:
    urls.extend([f"{base_url}#page={i}" for i in range(2, 50)])
urls = url + urls
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
for url in urls:
    try:
        driver.get(url)
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="product__ProductCardViewWrapper-pdz12a-0 kxqkyc")
        for row in data:
            nafn = row.find('a', class_ = "plain hover-underline").text.strip()
            if(row.find("div", class_="container-offer").find("span")):
                sale = True
                regular_price_element = row.find("strike")
                regular = regular_price_element.text.strip()
                reg = regular.split(" ")
                regular_price = reg[0]
                sale_price_element = row.find("strong")
                sale1 = sale_price_element.text.strip()
                sal = sale1.split(" ")
                sale_price = reg[0]
            else:
                sale = False
                sale_price = None
                regular_price_element = row.find("strong")
                regular = regular_price_element.text.strip()
                reg = regular.split(" ")
                regular_price = reg[0]

            if nafn and (sale_price or regular_price):
                temp = {
                    "Nafn": nafn,
                    "Verð": regular_price,
                    "Útsöluverð": sale_price,
                    "On_sale": sale
                }
                
                vorur.append(temp)
                print(temp)
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
for i in vorur:
    print(i)