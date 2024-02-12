from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#Skrapar bila en lika aukahluti og thad getur verid allt fra bol upp i dekk

vorur = []
# url = ["https://www.hekla.is/is/bilar/nyir-bilar-syningasalur", "https://www.hekla.is/is/bilar/notadir-bilar"]

# urls = []
# for base_url in url:
#     urls.extend([f"{base_url}?page={i}" for i in range(2, 100)])
# url1 = ["https://www.hekla.is/is/bilar/aukahlutir?sort=random-asc"]
# for base_url in url1:
#     urls.extend([f"{base_url}&page={i}" for i in range(2, 100)])
# urls = url + urls + url1
urls = ["https://www.toyota.is/new-cars?showMoreFilters=false"]
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="ModelResultStyles__Header-sc-1por3lq-4 kcYORJ")
        for row in data:
            nafn1 = row.find('a', class_="ModelResultStyles__RedirectWrapper-sc-1por3lq-6 gdWzQL")
            if(nafn1):
                nafn = nafn1.text.strip()
            else:
                nafn =  None
            if(row.find("div", class_="priceBefore")):
                sale = True
                regular_price_element = row.find_all("span",class_="n")
                regular_price = regular_price_element[0].text.strip()
                sale_price = regular_price_element[1].text.strip()
            else:
                sale = False
                sale_price = None
                regular_price_element = row.find("div", class_ = "ModelResultPriceStyles__Cash-sc-45o5ol-1 jjtNHu t-zeta-text")
                if(regular_price_element):
                    regular_price = regular_price_element.text.strip().split(" ")
                    regular_price = regular_price[1]
                else: 
                    None

            if nafn and (sale_price or regular_price):
                temp = {
                    "Nafn": nafn,
                    "Verð": regular_price,
                    "Útsöluverð": sale_price,
                    "On_sale": sale
                }
                
                vorur.append(temp)
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
for i in vorur:
    print(i)