from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

vorur = []
urls = ["https://www.kringlan.is/vorur"]
for i in range(24, 72000, 24):
    tem = f"https://www.kringlan.is/vorur?from={i}"
    urls.append(tem)

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProductItem_textLink__BcW3W")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("a", class_="ProductItem_textLink__BcW3W")

        for row in data:
            nafn = row.find('h2', class_='ProductItem_headline__2RJ5m mb-2 mb-md-3')
            sale_price_element = row.find("h4", class_="ProductItem_price__2mJ8v ProductItem_salePrice__1OI_C")
            regular_price_element = row.find("span", class_="ProductItem_regularPrice__3O6KZ")
            
            if sale_price_element:
                sale = True
                sale_price = sale_price_element.text.strip()
                regular_price = regular_price_element.text.strip() if regular_price_element else None
            else:
                sale = False
                regular_price_element = row.find("h4", class_="ProductItem_price__2mJ8v")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
                sale_price = None

            if nafn and (sale_price or regular_price):
                temp = {
                    "Nafn": nafn.text.strip(),
                    "Verð": regular_price,
                    "Útsöluverð": sale_price,
                    "On_sale": sale
                }
                vorur.append(temp)

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
print(vorur)
