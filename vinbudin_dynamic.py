from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

vorur = {}
urls = ["https://www.vinbudin.is/heim/vorur/vorur"]
for i in range(2, 200):
    urls.append(f"{urls[0]}?page={i}")

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "information")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find_all("div", class_="information")
        for row in data:
            title_div = row.find('div', class_='top')
            nafn = title_div.find('span')
            price = row.find("span", class_="price")

            if nafn and price:
                vorur[nafn.text.strip()] = price.text.strip()
                print(nafn.text.strip(), price.text.strip())

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
