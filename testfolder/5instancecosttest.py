

splitvalueregios='<ul class="button lb-dropdown-label"'
splitvalueinstancetypes="div data-region="
regioindex='class=""'
regioindex2='class="js-active"'
listvanregios=[]
f = open("demofile.txt", "r", encoding="utf8")
content = f.read()

listplit=content.split(splitvalueinstancetypes[1:])
listplit2=listplit

regiolist=listplit[0].split('<li data-region=')

#dit script maakt een lijst van alle regios
for verregio in regiolist[1:]:
    #print(verregio)
    print(type(verregio))
    regiosindex3=verregio.index('role')
    print(regiosindex3)
    regios= verregio[1:regiosindex3]
    listvanregios.append(regios)


for region in listplit2:
    #print('coolbeans')
    try:
        regiofinder=region.index(regioindex)
        #print(region[0:regiofinder])
    except:
        regiofinder = region.index(regioindex2)
        #print(region[0:regiofinder])
#print(len(listplit))
f.close()

#print(listplit2[1])
txasdf="dit is een indextest"
#print(txasdf[1:])
#print(txasdf.index('ind'))



