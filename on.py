from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

vorur = []
urls = ["https://www.on.is/verdskra/"]


for url in urls:
    try:
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("div", class_="col-lg-8 offset-lg-2")
        for row in data:
            more = soup.find_all("tr")
            for da in more:
                allt = da.find_all("td")
                temp = {}
                if not allt[0].find("strong"):
                    if(len(allt) == 4):
                        nafn = allt[0].text.strip()
                        verd1 = allt[3].text.strip()
                        temp["Nafn"] = nafn
                        temp["Price"] = verd1
                    if(len(allt) == 3):
                        nafn = allt[0].text.strip()
                        verd1 = allt[1].text.strip()
                        verd2 = allt[2].text.strip()
                        temp["Nafn"] = nafn
                        temp["Price"] = verd1
                        temp["Price2"] = verd2
                    if(len(allt) == 2):
                        nafn = allt[0].text.strip()
                        verd1 = allt[1].text.strip()
                        temp["Nafn"] = nafn
                        temp["Price"] = verd1
                vorur.append(temp)
    except Exception as e:
        print(f"Error processing {url}: {e}")

vorur1 = []
count = 0
for i in vorur:
    if(len(i)!=0):
        if("Almenn rafmag" in i["Nafn"]):
            count += 1
        if(count != 2):
            vorur1.append(i)
        else:
            break

for i in vorur1:
    if(len(i) == 2):
        spl = i["Price"].split(" ")
        price = spl[0].replace(",", '.')
        i["Price"] = price
    if(len(i) == 3):
        spl = i["Price"].split(" ")
        price = spl[0].replace(",", '.')
        i["Price"] = price

        spl = i["Price2"].split(" ")
        price = spl[0].replace(",", '.')
        i["Price2"] = price

for i in vorur1:
    print(i)
