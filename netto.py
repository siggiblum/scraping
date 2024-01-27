from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

urls = ["https://netto.is/voerur/avextir-og-graenmeti/?pageSize=1000", "https://netto.is/voerur/mjolkurvoerur/?pageSize=1000", 
        "https://netto.is/voerur/kjoet-og-fiskur/?pageSize=1000", "https://netto.is/voerur/braud-og-koekur/?pageSize=1000", 
        "https://netto.is/voerur/kaelivoerur/?pageSize=1000", "https://netto.is/voerur/alegg/?pageSize=1000", 
        "https://netto.is/voerur/frystivoerur/?pageSize=1000", "https://netto.is/voerur/heilsa-og-utlit/?pageSize=1000", 
        "https://netto.is/voerur/drykkjarvoerur/?pageSize=1000", "https://netto.is/voerur/thurr-og-nidursuduvoerur/?pageSize=1000", 
        "https://netto.is/voerur/saelgaeti-og-snakk/?pageSize=1000", "https://netto.is/voerur/barnavoerur/?pageSize=1000", 
        "https://netto.is/voerur/gaeludyravoerur/?pageSize=1000", "https://netto.is/voerur/nikotin-og-eldfaeri/?pageSize=1000", 
        "https://netto.is/voerur/heimilisvoerur/?pageSize=1000", "https://netto.is/voerur/jolavoerur/?pageSize=1000"]

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "mt-15")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        vorur = {}
        data = soup.find_all("div", class_="mt-15")
        for row in data:
            nafn = row.find('span', class_='font-bold text-20 xl:text-22')
            price = row.find("span", class_="mb-4 leading-6 ellipsis text-13 xl:text-14")

            if nafn and price:
                vorur[nafn.text.strip()] = price.text.strip()
                print(nafn.text.strip(), price.text.strip())

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
