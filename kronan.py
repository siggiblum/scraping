import pandas as pd 
import requests
from datetime import datetime
prices = []
names = []
dic = {}
listi_url = [f'/api/categories/01-00-00-avextir/details/?page=1', f'/api/categories/02-00-00-graenmeti/details/?page=1', '/api/categories/04-00-00-kjot/details/?page=1',
             f'/api/categories/03-00-00-fiskur/details/?page=1', f'/api/categories/05-00-00-mjolkurvorur-og-egg/details/?page=1', f'/api/categories/06-00-00-braud-kokur-og-kex/details/?page=1', 
             f'/api/categories/07-00-00-a-braud/details/?page=1', f'/api/categories/08-00-00-eldamennskan/details/?page=1', f'/api/categories/09-00-00-bakstur/details/?page=1', 
             f'/api/categories/10-00-00-morgunmatur-og-heilsubot/details/?page=1', f'/api/categories/11-00-00-a-ferdinni/details/?page=1', f'/api/categories/12-00-00-tilbunir-rettir/details/?page=1', 
             f'/api/categories/13-00-00-vegan/details/?page=1', f'/api/categories/14-00-00-frystivara/details/?page=1', f'/api/categories/15-00-00-heitir-drykkir/details/?page=1', 
             f'/api/categories/16-00-00-drykkir/details/?page=1', f'/api/categories/17-00-00-bornin/details/?page=1', f'/api/categories/18-00-00-heimilid/details/?page=1', 
             f'/api/categories/19-00-00-snyrtivara/details/?page=1', f'/api/categories/20-00-00-dyrin/details/?page=1', f'/api/categories/21-00-00-laugardags/details/?page=1', 
             f'/api/categories/24-00-00-jolin/details/?page=1', f'/api/categories/25-00-00-hrekkjavaka/details/?page=1']

for i in listi_url:
    header = {
        'authority': 'backend.kronan.is',
        'method': 'GET',
        'path': i,
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'Origin': 'https://kronan.is'
    }
    byrjun = 'https://backend.kronan.is'
    url = byrjun + i
    api_req = requests.get(url, headers=header)
    # print(api_req.json())
    json_data = api_req.json()
    print(json_data)
    pagecount = json_data.get('pageCount')
    for x in range(1, pagecount + 1):
        crop =  i[:-1]
        strengur = byrjun + crop + str(x)
        api_req =  requests.get(strengur, headers=header)
        json_data = api_req.json()
        for product in json_data.get('products', []):
            price = product.get('variants', [{}])[0].get('discountedPrice')
            name = product.get('name')
            dic[name] = price
            prices.append(price)
            names.append(name)
            print(name)

# Distinct count er 8057
names = []
prices = []
for key, value in dic.items():
    names.append(key)
    prices.append(value)
data = {'Name': names, 'Price': prices}
df = pd.DataFrame(data)
dagsetning = datetime.today().date()
df.insert(0, 'Date', dagsetning)
df['Verslun'] = 'Kronan'
print(df)
df.to_csv('C:/Users/SiggiBlum/Desktop/Stefnir/output_file2.csv', index=False)
