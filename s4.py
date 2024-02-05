from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

vorur = []
name_counts = {}
urls = ["https://s4s.is/skor/skor-s4s-is-skor-herraskor", "https://s4s.is/skor/skor-s4s-is-skor-doemuskor",
"https://s4s.is/skor/boern"]

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

for url in urls:
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "productInformation")))
        time.sleep(5)
        while True:
            try:
                time.sleep(5)
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Sækja Fleiri Vörur')]]"))
                )
                # Use JavaScript to click the button
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(5)  # Adjust based on actual load times
            except Exception as e:
                print("No more products to load or error clicking the button:", e)
                break

        # Scrape the updated page source after every load more action
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="productInformation")
        for row in data:
            item_dict = {}  # Initialize a dictionary for this item
            nafn_tag = row.find('p', class_='productName')  # This is the Tag object
            if nafn_tag:
                nafn_text = nafn_tag.text.strip()  # Extract text and strip whitespace from the Tag
                # Handle duplicate names
                if nafn_text in name_counts:
                    name_counts[nafn_text] += 1
                    nafn_text += f" ({name_counts[nafn_text]})"  # Append the count to the name text
                else:
                    name_counts[nafn_text] = 1  # First occurrence of this name text

                item_dict['name'] = nafn_text
                # Check for sales and set prices accordingly
                if row.find("p", class_="productPrice bold discountedPrice"):
                    sales = True
                    discount_price = row.find('p', class_='productPrice bold discountedPrice').text.strip()
                    normal_price = row.find('p', class_='oldPrice').text.strip()
                    item_dict['discount_price'] = discount_price
                else:
                    sales = False
                    normal_price = row.find('p', class_='productPrice bold').text.strip()
                    item_dict['discount_price'] = None  # No discount price
                
                item_dict['normal_price'] = normal_price
                item_dict['sales'] = sales

                vorur.append(item_dict)

    except Exception as e:
        print(f"Error processing {url}: {e}")

# print(vorur)
for i in vorur:
    print(i)
print(len(vorur))

driver.quit()
