from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

#Virkar nokkuð vel

vorur = []
urls = []
ur = ["https://tekk.is/collections/husgogn-1", "https://tekk.is/collections/smavara-1", "https://tekk.is/collections/sofar"]
for x in ur:
    urls.append(x)
    spl = x.split("-")
    ur = spl[0]
    for i in range(2, 50):
        tem = ur + f"?page={i}"
        urls.append(tem)

for i in urls:
    print(i)
options = Options()
options.headless = True
# Here is how you add the User-Agent header using options
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Updated to use `Service` as recommended in newer Selenium versions
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

for url in urls:
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="product-thumbnail available-true")
        for row in data:
            nafn = row.find('a', class_='product-thumbnail__title')
            sale_price_element = row.find("span", class_="product-thumbnail__price price sale")
            
            if sale_price_element:
                sale = True
                sale_price_element = row.find("span", class_="money")  # Assuming this finds the correct sale price as before
                sale_price = sale_price_element.text.strip() if sale_price_element else None
                regular_price_element = row.find("span", class_="product-thumbnail__was-price was-price")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
            else:
                sale = False
                regular_price_element = row.find("span", class_="money")
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
    
        data = soup.find_all("div", class_="product-thumbnail available-false")
        for row in data:
            nafn = row.find('a', class_='product-thumbnail__title')
            sale_price_element = row.find("span", class_="product-thumbnail__price price sale")
            
            if sale_price_element:
                sale = True
                sale_price_element = row.find("span", class_="money")  # Assuming this finds the correct sale price as before
                sale_price = sale_price_element.text.strip() if sale_price_element else None
                regular_price_element = row.find("span", class_="product-thumbnail__was-price was-price")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
            else:
                sale = False
                regular_price_element = row.find("span", class_="money")
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
for i in vorur:
    print(i)
print(len(vorur))