from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

vorur = {}
urls = ["https://www.on.is/verdskra/"]
for i in range(2, 50):
    urls.append(f"{urls[0]}?page={i}")

for url in urls:
    try:
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find_all("div", class_="col-lg-8 offset-lg-2")
        for row in data:
            tr = row.find("tr")
            for tri in tr:
                name, price = None, None
                # Find all <td> tags within the table row
                tds = tr.find("td")
                print(tds.text.strip())
                # print(tds)
                # for td in tds:
                #     # Check if the <td> has a 'style' attribute
                #     if 'style' in td.attrs:
                #         # If it has a style, treat it as price
                #         price = td.text.strip()
                #     else:
                #         # If no style, treat it as name
                #         name = td.text.strip()

                # # If both name and price are found, add them to the dictionary
                
                # if name and price:
                #     vorur[name] = price
                    # print(name, price)
    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()
