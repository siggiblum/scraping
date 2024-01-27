from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

vorur = {}
urls = ["https://aurbjorg.is/rafmagn"]

for url in urls:
    try:
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find("tbody", class_="Table_tbody___v1BZ")
        tr = data.find_all("tr")
        for row in tr:
            nafn = row.find("div", class_= "Headline_headline__A7A_e Headline_small___AoHg Headline_bold__wBkQ5 __className_c1491f")
            prices = row.find_all("td", class_ = "Table_td__TflLc Table_leftAlign__fgXwz")
            count = 0
            dic = {}
            for i in prices:
                if(count == 1):
                    dic["Verð (kWst)"] = i.text.strip()
                elif(count == 2):
                    dic["Meðalkostnaður"] = i.text.strip()
                count+=1
            vorur[nafn.text.strip()] = dic

    except Exception as e:
        print(f"Error processing {url}: {e}")

for key, value in vorur.items():
    print(key, value)