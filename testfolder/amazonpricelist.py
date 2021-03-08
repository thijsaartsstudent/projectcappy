import json
import requests
from datetime import date
import urllib.request
today = date.today()

def namefromdescription(teststring):
    if 'for' in teststring:

        return 'network'
    else:
        teststrin2 = teststring.split('per')
        ts3 = teststrin2[1]
        ts4 = ts3.split('.')
        # print(ts4[1].rindex(' '))
        # searchvalue=ts4[1].rfind('r')
        # print(ts4)
        # print(len(ts4[0]))
        ts5 = ts4[0]

        #print(ts5)
        searchvalue = (ts5.rindex(' '))
        namevalue = ts5[0:searchvalue]
        #print(namevalue)
        #print(teststring)
        if namevalue[0] == ' ':
            namevalue = namevalue[1:]

        return namevalue
#simple script dat een lijst maakt van alle regio's en dan opslaat
def regiolist():
    today = date.today()

    url='https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json'
    r = requests.get(url, allow_redirects=True)
    open(str(today)+'testjsondownload1.json', 'wb').write(r.content)
    #print(type(r.content))

    #for more information about aws prices https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html
    with open("region_index.json") as f:
      data2 = json.load(f)
    lijstvanregios=[]
    lijstvanregiosdict={}
    for x in data2['regions']:
        #print(x)
        lijstvanregios.append(data2['regions'][x]['currentVersionUrl'])
        url=data2['regions'][x]['currentVersionUrl']
        regioncode=data2['regions'][x]["regionCode"]
        lijstvanregiosdict[regioncode]=url
    #print(lijstvanregiosdict)
    #print(lijstvanregios)
    saveregiolist='pricinginformation/'+str(today)+'regiolist.json'
    with open(saveregiolist, 'w') as fp:
        json.dump(lijstvanregiosdict, fp)
    with open("indexuseast.json") as f:
        data = json.load(f)

    for regio in lijstvanregiosdict:

        url = 'https://pricing.us-east-1.amazonaws.com'+lijstvanregiosdict[regio]

        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        print(type(data))

        pricedict2 = {}
        dictproducttotype={}
        dictfortypetocode = {}
        #deze regel is voor de code
        naamvanregiopricing='pricinginformation/'+str(today)+regio+'pricing.json'
        pricedict2 = {}
        print(regio)
        print(url)
        #dit stukje is voor on demand
        for x in data['terms']['OnDemand']:
            for y in data['terms']['OnDemand'][x]:
                for z in data['terms']['OnDemand'][x][y]['priceDimensions']:
                    #            print(x, y, z)
                    # print(data['terms']['OnDemand'][x][y]['priceDimensions'][z]['description'])
                    description = data['terms']['OnDemand'][x][y]['priceDimensions'][z]['description']
                    priceperunit = data['terms']['OnDemand'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                    #print('hallo dit is de code',[x])
                    #print(data['products'][x]['attributes'].keys())
                    try:
                        instancevalue = data['products'][x]['attributes']['instanceType']
                    except:
                        print('deze product',x,url,'heeft geen instancetype')
                        continue
                    instancevalue = data['products'][x]['attributes']['instanceType']
                    if instancevalue not in dictfortypetocode:
                       dictfortypetocode[instancevalue]={}
                    tosearch = 'On Demand Linux ' + instancevalue
                    # print(tosearch)
                    # print(description)
                    if tosearch in description:
                        dictfortypetocode[instancevalue]['linux cost per demand'] = {}
                        dictfortypetocode[instancevalue]['linux cost per demand']['cost per hour'] = priceperunit


                    instancevalue = data['products'][x]['attributes']['instanceType']

                    tosearch = 'per On Demand Windows ' + instancevalue

                    if tosearch in description:
                        dictfortypetocode[instancevalue]['windows cost per demand']={}
                        dictfortypetocode[instancevalue]['windows cost per demand']['cost per hour'] = priceperunit
                    else:
                        nametouse=namefromdescription(description)
                        instancevalue = data['products'][x]['attributes']['instanceType']
                        dictfortypetocode[instancevalue][nametouse]={}
                        dictfortypetocode[instancevalue][nametouse]['cost per hour'] = priceperunit

        #dit is voor de reserved prices
        upfront = 0
        perhour = 0
        dictfortypetocode = {}
        if 'Reserved' not in data['terms']:
            print('je kan hier niet reserveren',url)
            continue
        for x in data['terms']['Reserved']:
            instancevalue = data['products'][x]['attributes']['instanceType']
            if instancevalue not in dictfortypetocode:
                dictfortypetocode[instancevalue] = {}
                dictfortypetocode[instancevalue]['linux'] = {}
                dictfortypetocode[instancevalue]['windows'] = {}

            for y in data['terms']['Reserved'][x]:
                linux = 0
                windows = 0
                upfrontfee = 0
                for z in data['terms']['Reserved'][x][y]['priceDimensions']:
                    if len(data['terms']['Reserved'][x][y]['priceDimensions']) == 2:
                        # print(data['terms']['Reserved'][x][y]['priceDimensions'][z])
                        description = data['terms']['Reserved'][x][y]['priceDimensions'][z]['description']
                        priceperunit = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                        # print(description)

                        # dit stukje is voor het linux gedelete
                        if 'Linux/UNIX (Amazon VPC)' in description:
                            #print('test')
                            linux = 1
                            perhour = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                        if 'Linux/UNIX (Amazon VPC)' not in description:
                            perhour = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']

                        if data['terms']['Reserved'][x][y]['priceDimensions'][z]['description'] == 'Upfront Fee':
                            upfrontfee = 1

                            upfront = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']

                        if linux == 1 and upfrontfee == 1:
                            leaselength = data['terms']['Reserved'][x][y]['termAttributes']['LeaseContractLength']
                            offering = data['terms']['Reserved'][x][y]['termAttributes']['OfferingClass']
                            purchaseoption = data['terms']['Reserved'][x][y]['termAttributes']['PurchaseOption']
                            nameforproduct = leaselength + offering + purchaseoption
                            dictfortypetocode[instancevalue]['linux'][nameforproduct] = {}
                            dictfortypetocode[instancevalue]['linux'][nameforproduct]['upfront'] = upfront
                            dictfortypetocode[instancevalue]['linux'][nameforproduct]['per hour'] = perhour
                        if linux != 1 and upfrontfee == 1:
                            leaselength = data['terms']['Reserved'][x][y]['termAttributes']['LeaseContractLength']
                            offering = data['terms']['Reserved'][x][y]['termAttributes']['OfferingClass']
                            purchaseoption = data['terms']['Reserved'][x][y]['termAttributes']['PurchaseOption']
                            nameforproduct = leaselength + offering + purchaseoption
                            # namefortype wordt het operationgsysteem
                            if 'Upfront Fee' in description:
                                continue
                            namefortype = description.split(',')
                            namefortype2 = namefortype[0]
                            if namefortype2 not in dictfortypetocode[instancevalue]:
                                dictfortypetocode[instancevalue][namefortype2] = {}
                            dictfortypetocode[instancevalue][namefortype2][nameforproduct] = {}
                            dictfortypetocode[instancevalue][namefortype2][nameforproduct]['upfront'] = upfront
                            dictfortypetocode[instancevalue][namefortype2][nameforproduct]['per hour'] = perhour
                        # print(data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD'])

        with open(naamvanregiopricing, 'w') as fp:
            json.dump(dictfortypetocode, fp)

regiolist()
with open("indexuseast.json") as f:
  data = json.load(f)


#print(data['products']['2XQV6XXB25PRTQFQ']['attributes']['instanceType'])
#print(data['terms']['OnDemand']['UU7DSR82ZGC88ZNB']["UU7DSR82ZGC88ZNB.JRTCKXETXF"]['priceDimensions'].keys())

#print("Today's date:", today)
namedate= 'listofinstanceandcodewords'+str(today)+'.txt'
#print(dictfortypetocode)
f = open(namedate, "a+")
def productfuntion():
    for x in data['products']:
        #print(x)
        try:
            if not data['products'][x]['attributes']['instanceType']:
                continue
        except:
            continue
        instancevalue=data['products'][x]['attributes']['instanceType']
        #print(instancevalue)
        if instancevalue in dictfortypetocode:
            dictfortypetocode[instancevalue][x]={}
            continue
        dictfortypetocode[instancevalue]={}
        dictfortypetocode[instancevalue][x] = {}
        # f.write(instancevalue+':'+x+'\n')



#print(dictfortypetocode.keys())

'SQL Server Enterprise'
'BYOL'
'On Demand Linux'
'per On Demand Windows'
dictfortypetocode={}
dictproducttotype={}
for x in data['products']:
    try:
        z= data['products'][x]['attributes']['instanceType']
    except:
        continue
    #print(x)
    instancetype=data['products'][x]['attributes']['instanceType']
    dictproducttotype[x]=instancetype
    dictfortypetocode[instancetype] = {}
    dictfortypetocode[instancetype][x] = {}
#print(dictproducttotype)
#print(dictfortypetocode)
def indexeerkostenondemand(data):
    pricedict2={}
    for x in data['terms']['OnDemand']:
        for y in data['terms']['OnDemand'][x]:
            for z in data['terms']['OnDemand'][x][y]['priceDimensions']:
    #            print(x, y, z)
                #print(data['terms']['OnDemand'][x][y]['priceDimensions'][z]['description'])
                description = data['terms']['OnDemand'][x][y]['priceDimensions'][z]['description']
                priceperunit = data['terms']['OnDemand'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                if 'On Demand Linux' in description:
                    instancevalue=data['products'][x]['attributes']['instanceType']
                    tosearch = 'On Demand Linux ' + instancevalue
                    #print(tosearch)
                    #print(description)
                    if tosearch in description:
                            dictfortypetocode[instancevalue]['linux cost per demand'] = priceperunit
                if 'per On Demand Windows' in description:
                    instancevalue = dictproducttotype[x]

                    tosearch='per On Demand Windows ' + instancevalue


                    if tosearch in description:
                        dictfortypetocode[instancevalue]['windows cost per demand'] = priceperunit
    return(dictfortypetocode)

with open("indexuseast.json") as f:
  data = json.load(f)

#print(data['terms']['Reserved']['ZU2D6CMARKQPNWAA'].keys())
#print(indexeerkostenondemand(data))
#print(dictfortypetocode)
def reserverdcost(data):
    upfront=0
    perhour=0
    dictforreserverd={}
    for x in data['terms']['Reserved']:
        instancevalue = data['products'][x]['attributes']['instanceType']
        if instancevalue not in dictforreserverd:
            dictforreserverd[instancevalue] = {}
            dictforreserverd[instancevalue]['linux']={}
            dictforreserverd[instancevalue]['windows'] = {}

        for y in data['terms']['Reserved'][x]:
            linux=0
            windows=0
            upfrontfee=0
            for z in data['terms']['Reserved'][x][y]['priceDimensions']:
                if len(data['terms']['Reserved'][x][y]['priceDimensions']) ==2:
                    #print(data['terms']['Reserved'][x][y]['priceDimensions'][z])
                    description = data['terms']['Reserved'][x][y]['priceDimensions'][z]['description']
                    priceperunit = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                    #print(description)

                    #dit stukje is voor het linux gedelete
                    if 'Linux/UNIX (Amazon VPC)' in description:
                        print('test')
                        linux=1
                        perhour = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']
                    if 'Linux/UNIX (Amazon VPC)' not in description:
                        perhour = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']

                    if data['terms']['Reserved'][x][y]['priceDimensions'][z]['description'] =='Upfront Fee':
                        upfrontfee=1

                        upfront = data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD']

                    if linux ==1 and upfrontfee ==1:

                        leaselength = data['terms']['Reserved'][x][y]['termAttributes']['LeaseContractLength']
                        offering = data['terms']['Reserved'][x][y]['termAttributes']['OfferingClass']
                        purchaseoption = data['terms']['Reserved'][x][y]['termAttributes']['PurchaseOption']
                        nameforproduct = leaselength + offering + purchaseoption
                        dictforreserverd[instancevalue]['linux'][nameforproduct] = {}
                        dictforreserverd[instancevalue]['linux'][nameforproduct]['upfront'] = upfront
                        dictforreserverd[instancevalue]['linux'][nameforproduct]['per hour'] = perhour
                    if linux != 1 and upfrontfee == 1:
                        leaselength = data['terms']['Reserved'][x][y]['termAttributes']['LeaseContractLength']
                        offering = data['terms']['Reserved'][x][y]['termAttributes']['OfferingClass']
                        purchaseoption = data['terms']['Reserved'][x][y]['termAttributes']['PurchaseOption']
                        nameforproduct = leaselength + offering + purchaseoption
                        #namefortype wordt het operationgsysteem
                        if 'Upfront Fee' in description:
                            continue
                        namefortype=description.split(',')
                        namefortype2=namefortype[0]
                        if namefortype2 not in dictforreserverd[instancevalue]:
                            dictforreserverd[instancevalue][namefortype2] = {}
                        dictforreserverd[instancevalue][namefortype2][nameforproduct] = {}
                        dictforreserverd[instancevalue][namefortype2][nameforproduct]['upfront'] = upfront
                        dictforreserverd[instancevalue][namefortype2][nameforproduct]['per hour'] = perhour
                    #print(data['terms']['Reserved'][x][y]['priceDimensions'][z]['pricePerUnit']['USD'])

    return dictforreserverd

#x.terms.Reserved.9FMN2EN6UD88KHVK["9FMN2EN6UD88KHVK.MZU6U2429S"].priceDimensions["9FMN2EN6UD88KHVK.MZU6U2429S.2TG2D8R56U"].pricePerUnit.USD
#x.terms.Reserved.4ZK8C6MPPBBT3CBQ["4ZK8C6MPPBBT3CBQ.38NPMPTW36"].termAttributes.LeaseContractLength
#OfferingClass
#PurchaseOption
#costifnormation=reserverdcost(data)
#print(costifnormation)
#with open('test5.json', 'w') as fp:
#    json.dump(costifnormation, fp)

