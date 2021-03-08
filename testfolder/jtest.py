import json
import pandas as pd

with open('output.json',encoding="utf8") as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
#print(data.items())
#print(data['html']['body'].keys())
#print(data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'][1]['ul'][1]['li'][1]['div']['div'][0]['div']['div'][1]['div'][0]["table"]["tbody"])
#print(data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'][1]['ul'][1]['li'][1]['div']['div'][0]['div']['div'][1]['div'][0])
#print(data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'].keys)
#print(data['html']['body']['div']['1']['main']['div']['0']['div']['div']['div'].values())
#print(data['html']['head'].keys())

#for x in data['html']:
  #print(x,type(x))
#print(data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'][1]['ul'][1]['li'][1]['div']['div'][0]['div']["div"][1]['div'][0])

linuxkostenperregio=data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'][1]['ul'][1]['li'][1]['div']['div'][0]['div']["div"][1]['div']
#for x in linuxkostenperregio:
#  print(x)
#print(linuxkostenperregio[0]['@data-region'])
for x in linuxkostenperregio:
  print (x['@data-region'])
#print(linuxkostenperregio[0]['table'].keys())
#print(data['html']['body']['div'][1]["main"]['div'][0]['div']['div']['div'][1]['ul'][1]['li'])
lijstvanregios=     data["html"]["body"]["div"][1]["main"]["div"][0]["div"]["div"]["div"][1]['ul'][1]["li"][1]['div']['div'][0]['div']['div'][0]['div']['ul']['li']
#print(lijstvanregios)

for x in lijstvanregios:
  print(x)


#ik wil de prijs weten van mijn setup, regio is frankfurt en 2 servers die a1.large zijn

