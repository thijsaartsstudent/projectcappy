import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://aws.amazon.com/ec2/pricing/on-demand/'

r = requests.get(url)
html = r.text
#<div data-region="us-east-2"
soup = BeautifulSoup(html)
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows[1:]:
#    cols = row.find_all('td')
#    cols = [ele.text.strip() for ele in cols]
#    data.append([ele for ele in cols if ele])
    print(row)

#result = pd.DataFrame(data, columns=['Date', '1 Mo', '2 Mo', '3 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr', '30 Yr'])

#print(result)