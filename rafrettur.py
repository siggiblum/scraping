from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

vorur = {}
urls = ["https://rafrettur.is/collections/all"]
for i in range(2, 50):
    urls.append(f"{urls[0]}?page={i}")

for url in urls:
    try:
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="card__information")

        for row in data:
            nafn = row.find('a', class_='full-unstyled-link')  # Corrected class name
            price = row.find("span", class_="price-item price-item--regular")

            if nafn and price:
                price_text = price.text.strip()
                price_parts = price_text.split()
                numeric_price = next((part for part in price_parts if part.isdigit()), None)

                if numeric_price:
                    vorur[nafn.text.strip()] = numeric_price
                    print(nafn.text.strip(), numeric_price)

    except Exception as e:
        print(f"Error processing {url}: {e}")
