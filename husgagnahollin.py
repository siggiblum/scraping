from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

vorur = []
url = ["https://husgagnahollin.is/voruflokkur/sofar/","https://husgagnahollin.is/voruflokkur/stolar/",
        "https://husgagnahollin.is/voruflokkur/bord/", "https://husgagnahollin.is/voruflokkur/husgogn/",
        "https://husgagnahollin.is/voruflokkur/gjafavorur/", "https://husgagnahollin.is/voruflokkur/gjafavorur/gjafahugmyndir/"]

urls = ["https://husgagnahollin.is/voruflokkur/sofar/","https://husgagnahollin.is/voruflokkur/stolar/",
        "https://husgagnahollin.is/voruflokkur/bord/", "https://husgagnahollin.is/voruflokkur/husgogn/",
        "https://husgagnahollin.is/voruflokkur/gjafavorur/", "https://husgagnahollin.is/voruflokkur/gjafavorur/gjafahugmyndir/"]

for x in url:
    for i in range(2,50):
        tem = x + f"page/{i}/"
        urls.append(tem)
        print(tem)


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item-info")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="item-info")

        for row in data:
            nafn = row.find('a').text.strip()
            del_element = row.find("del")
            bdi_elements = row.find_all("bdi")

            if del_element:
                sale = True
                regular_price = del_element.text.strip().replace('\xa0', '')
                # Assuming the sale price is the next 'bdi' element after the 'del' element
                sale_price = bdi_elements[1].text.strip().replace('\xa0', '') if len(bdi_elements) > 1 else None
            else:
                sale = False
                regular_price = bdi_elements[0].text.strip().replace('\xa0', '') if bdi_elements else None
                sale_price = None

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
