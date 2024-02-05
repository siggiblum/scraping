from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

#Vantar útsölur

def adding(fm):
    result = []
    for x in fm:
        result.append(fm[0])
        for i in range(2, 50):
            temp = x
            temp = temp + f"?page={i}"
            result.append(temp)
    return result

vorur = []
name_counts = {}
urls_women = ["https://www.hverslun.is/konur/fatnadur/skoda-allan-fatnad", "https://www.hverslun.is/karlar/skor/skor-kk",
            "https://www.hverslun.is/konur/aukahlutir/skoda-alla-aukahluti-kvk","https://www.hverslun.is/konur/baetiefni/oll-baetiefni-kvk",
            "https://www.hverslun.is/konur/hud-og-snyrtivorur/skoda-allar-vorur-hud-og-snyrtivorur"]
urls_men = ["https://www.hverslun.is/konur/hud-og-snyrtivorur/skoda-allar-vorur-hud-og-snyrtivorur", "https://www.hverslun.is/karlar/skor/skor-kk",
            "https://www.hverslun.is/karlar/aukahlutir-kk/skoda-alla-aukahluti-kk","https://www.hverslun.is/karlar/baetiefni/oll-baetiefni-karlar",
            "https://www.hverslun.is/karlar/hud-og-snyrtivorur-kk/skoda-allar-vorur-hud-og-snyrtivorur"]
urls_other = ["https://www.hverslun.is/born/fatnadur/skoda-allan-fatnad-born", "https://www.hverslun.is/born/skor/skoda-alla-sko-born", 
            "https://www.hverslun.is/born/aukahlutir/skoda-alla-aukahluti-born", "https://www.hverslun.is/born/baetiefni-born",
            "https://www.hverslun.is/born/tannheilsa-born", "https://www.hverslun.is/heilsa-og-lifsstill/heimili/allar-vorur",
            "https://www.hverslun.is/heilsa-og-lifsstill/aefingavorur","https://www.hverslun.is/heilsa-og-lifsstill/hud-og-snyrtivorur/skoda-allar-vorur-hud-og-snyrtivorur"]

urls = adding(urls_men) + adding(urls_other) + adding(urls_women)


options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="content")

        for row in data:
            item_dict = {}  # Initialize a dictionary for this item
            title_tag = row.find("h2", class_="title")
            if title_tag: 
                name_tag = title_tag.find("span")
                if name_tag:
                    nafn = name_tag.text.strip() 
                else:
                    nafn = None
            else:
                continue  # Skip this row if no title tag is found

            if nafn in name_counts:
                name_counts[nafn] += 1
                nafn += " " + str(name_counts[nafn])  # Append the count to the name
            else:
                name_counts[nafn] = 1  # First occurrence of this name

            price_tag = row.find("span", class_="n")
            if price_tag:
                regular_price = price_tag.text.strip() 
            else:
                regular_price = "Price not found"
            
            sale_price = None  
            sale = False 

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
print(vorur)