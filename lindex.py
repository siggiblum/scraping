from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

#Þegar glugginn poppar upp þarf að halda honum opnum allan tímann svo hann skrollar
#Niður því annars loadar hann ekki fleiri vörur, opnum þá ekki einu sinni minnka hann

vorur = []
name_counts = {}

urls = ["https://lindex.is/collections/domur-bolir", "https://lindex.is/collections/domur-blussur-og-skyrtur",
        "https://lindex.is/collections/domur-kjolar", "https://lindex.is/collections/domur-vesti", 
        "https://lindex.is/collections/domur-lettir-jakkar", "https://lindex.is/collections/domur-gallabuxur", 
        "https://lindex.is/collections/domur-buxur", "https://lindex.is/collections/domur-yfirhafnir", 
        "https://lindex.is/collections/domur-hlyrabolir", "https://lindex.is/collections/domur-peysur-og-gollur",
        "https://lindex.is/collections/domur-peysur-og-gollur/Category:-Knitwear", "https://lindex.is/collections/domur-blazer-jakkar",
        "https://lindex.is/collections/domur-leggings", "https://lindex.is/collections/domur-pils",
        "https://lindex.is/collections/domur-stuttbuxur", "https://lindex.is/collections/domur-medgongufatnadur",
        "https://lindex.is/collections/fylgihlutir-skart","https://lindex.is/collections/domur-fylgihlutir",
        "https://lindex.is/collections/fylgihlutir-harskraut", "https://lindex.is/collections/undirfot-ullarfatnadur",
        "https://lindex.is/collections/undirfot-sundfot", "https://lindex.is/collections/domur-ithrottafot",
        "https://lindex.is/collections/hjolabuxur", "https://lindex.is/collections/undirfot-brjostahaldarar",
        "https://lindex.is/collections/undirfot-naerbuxur", "https://lindex.is/collections/undirfot-sokkar",
        "https://lindex.is/collections/undirfot-sokkabuxur-og-leggings", "https://lindex.is/collections/undirfot-mom-undirfatnadur",
        "https://lindex.is/collections/nattfot-undirfot", "https://lindex.is/collections/undirfot-aefingafot",
        "https://lindex.is/collections/undirfot-sundfot", "https://lindex.is/collections/inniskor",
        "https://lindex.is/collections/sundfot-bikini", "https://lindex.is/collections/sundfot-sundbolir",
        "https://lindex.is/collections/undirfot-ullarfatnadur", "https://lindex.is/collections/a-haldsfatna-ur",
        "https://lindex.is/collections/annad-undirkjolar", "https://lindex.is/collections/undirfot-samfellur",
        "https://lindex.is/collections/annad-naerbolir", "https://lindex.is/collections/brjostahaldarar-aukahlutir",
        "https://lindex.is/collections/sloppar", "https://lindex.is/collections/snyrtivorur", 
        "https://lindex.is/collections/born-bolir", "https://lindex.is/collections/born-hlyrabolir",
        "https://lindex.is/collections/born-peysur", "https://lindex.is/collections/born-kjolar", 
        "https://lindex.is/collections/born-tunikur", "https://lindex.is/collections/born-pils",
        "https://lindex.is/collections/born-buxur", "https://lindex.is/collections/born-gallabuxur", "https://lindex.is/collections/nattfot",
        "https://lindex.is/collections/born-utifot", "https://lindex.is/collections/born-ullarfot", "https://lindex.is/collections/born-blussur",
        "https://lindex.is/collections/born-skyrtur", "https://lindex.is/collections/born-samfestingar", "https://lindex.is/collections/born-fylgihlutir",
        "https://lindex.is/collections/born-stuttbuxur", "https://lindex.is/collections/born-sokkar-og-sokkabuxur",
        "https://lindex.is/collections/born-sokkar-og-sokkabuxur", "https://lindex.is/collections/born-naerfot", 
        "https://lindex.is/collections/born-regnfot", "https://lindex.is/collections/born-sundfot", 
        "https://lindex.is/collections/basics-3-fyrir-2", "https://lindex.is/collections/care-collection", 
        "https://lindex.is/collections/ungaborn-44-86-samfellur", "https://lindex.is/collections/ungborn-kjolar",
        "https://lindex.is/collections/ungaborn-44-86-buxur-1", "https://lindex.is/collections/ungaborn-44-86-leggings", 
        "https://lindex.is/collections/ungborn-grunnfatnadur", "https://lindex.is/collections/ungaborn-44-86-nattfot",
        "https://lindex.is/collections/ungaborn-44-86-fylgihlutir-1", "https://lindex.is/collections/ungaborn-44-86-utifot-1", 
        "https://lindex.is/collections/ungaborn-44-86-newborn", "https://lindex.is/collections/ungaborn-44-86-peysur", 
        "https://lindex.is/collections/ungaborn-44-86-sett-1", "https://lindex.is/collections/ungaborn-44-86-sokkar-og-sokkabuxur",
        "https://lindex.is/collections/ungaborn-ullarfot", "https://lindex.is/collections/ungaborn-44-86-sundfot", 
        "https://lindex.is/collections/ungborn-fyrir-herbergid", "https://lindex.is/collections/ungaborn-44-86-3-fyrir-2"]

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-view-item__link"))) #Bíður hvort classinn er þar

        while True:
            elements = driver.find_elements(By.CLASS_NAME, "grid-view-item__link")
            number_of_loaded_items = len(elements)
            print(f"Number of loaded items: {number_of_loaded_items}")

            if elements:
                last_element = elements[-1]
                driver.execute_script("arguments[0].scrollIntoView(true);", last_element)
                time.sleep(6)  # Wait for new items to load

                # Check if new items have been loaded
                new_elements = driver.find_elements(By.CLASS_NAME, "grid-view-item__link")
                print(len(new_elements))
                if len(new_elements) == number_of_loaded_items:
                    print("No new items loaded, end of page reached.")
                    break


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("a", class_="grid-view-item__link")
        # print(data)
        for row in data:
            item_dict = {}  # Initialize a dictionary for this item
            
            nafn = row.find("div", class_="h4 grid-view-item__title").text.strip() if row.find("div", class_="h4 grid-view-item__title") else None
            if nafn:
                # Handle duplicate names
                if nafn in name_counts:
                    name_counts[nafn] += 1
                    nafn += str(name_counts[nafn])  # Append the count to the name
                else:
                    name_counts[nafn] = 1  # First occurrence of this name

                item_dict['name'] = nafn  # Add name to the dictionary

                # Check for sales and set prices accordingly
                if row.find("span", class_="collectionGridPriceNew"):
                    sales = True
                    discount_price = row.find('span', class_='collectionGridPriceNew').text.strip()
                    normal_price = row.find('span', class_='collectionGridPriceOld').text.strip()
                    item_dict['discount_price'] = discount_price
                else:
                    sales = False
                    normal_price = row.find('span', class_='collectionGridPriceNoDiscount').text.strip()
                    item_dict['discount_price'] = None  # No discount price
                
                item_dict['normal_price'] = normal_price
                item_dict['sales'] = sales
                
                vorur.append(item_dict)
                

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
