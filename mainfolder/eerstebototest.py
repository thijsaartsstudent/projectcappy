import boto3
from botocore.config import Config
ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
#print(response)
#print(type(response))
#print(response.keys())
lijstvanelasticaddresses=[]
lijstvanregios=[]
lijstvanregios2=[]
truelijstvanregios=[]
#response2= ec2.describe_regions()
#regionsresponse=(response2['Regions'])
#for x in regionsresponse:
#    lijstvanregios.append(x['RegionName'])


#trueallregions=ec2.describe_regions(AllRegions=True)
#trueregionsresponse=(trueallregions['Regions'])
#for x in trueregionsresponse:
#    truelijstvanregios.append(x['RegionName'])
#rint(len(truelijstvanregios))

#with open("amazon regions.txt", "r") as f:
#    mylist = f.read().splitlines()
def alleregios(ACCESS_KEY,SECRET_KEY):
    my_config = Config(
        region_name='us-west-1',
        signature_version='v4',

        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    cloudwatch = boto3.client('ec2',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              config=my_config)


    lijstvanregios2 = []
    ec2 = boto3.client('ec2')
    response2 = ec2.describe_regions()
    regionsresponse = (response2['Regions'])
    for x in regionsresponse:
        lijstvanregios2.append(x['RegionName'])
    return lijstvanregios2


#print(alleregios())
#print(mylist)
#print(lijstvanregios)
#print(mylist)
#deze value print de naam van de ec2 de eerste index is de hoeveelste instance, de tweede en derde index zijn om de values te vinden
#print(response['Reservations'][0]['Instances'][0]['Tags'][0]['Value'])
#print(response['Reservations'][1]['Instances'][0]['InstanceId'])
##print(response['Reservations'][1]['Instances'][0]['InstanceType'])
#print(response['Reservations'])
#print(response['Reservations'][1]['Instances'][0]['SecurityGroups'][0]['GroupId'])
#print(len(response))
#print(response['Reservations'][1]['Instances'][0].keys())



#print(lijstvanregios)

def alleinstances(regios):
    for regio in regios:
        lijstvanelasticaddresses = []
        ec2 = boto3.client('ec2', regio)
        instanceinformatie = ec2.describe_instances()
        netwerkinformatie= ec2.describe_vpcs()
        elinformatie = ec2.describe_addresses()
        #print(instanceinformatie['Reservations'])

        print(regio)
        #deze regel is om de vpc te printen
        for value1 in range (0,len(netwerkinformatie['Vpcs'])):
            print(netwerkinformatie['Vpcs'][value1]['VpcId'],netwerkinformatie['Vpcs'][value1]['CidrBlock'])

        #dit stukje is voor het printen van de elastic ip address
        #print(len(netwerkinformatie["Addresses"]))
        for value2 in range (0,len(elinformatie["Addresses"])):
            if len(elinformatie["Addresses"][value2]) < 10:
                print('deze elastic ip', elinformatie["Addresses"][value2]['PublicIp'],'is nergens mee verbonden')
            else:
                print('deze elastic ip',elinformatie["Addresses"][value2]['PublicIp'] ,'is verbonden met de instance',elinformatie["Addresses"][value2]['InstanceId'])


        #dit stukje hieronder is om de instances te checken
        if instanceinformatie['Reservations']==[]:
            print(': geen ec2 instances in deze regio')
            continue

        #print(len(instanceinformatie))
        #print(instanceinformatie)
        for value in range(0,len(instanceinformatie['Reservations'])):
            #print(len(instanceinformatie),'dit is de lengte van in')

            #print('dit is de value',value)
            id = instanceinformatie['Reservations'][value]['Instances'][0]['InstanceId']
            instancetype=instanceinformatie['Reservations'][value]['Instances'][0]['InstanceType']
            status=instanceinformatie['Reservations'][value]['Instances'][0]['State']['Name']
            # naam=instanceinformatie['Reservations'][value]['Instances'][0]['Tags'][0]['Value']
            print(id,instancetype,status)

            #print(counter)


def listalleinstances(regios):
    instanceinformationlist=[]
    for regio in regios:
        lijstvanelasticaddresses = []
        ec2 = boto3.client('ec2', regio)
        instanceinformatie = ec2.describe_instances()
        netwerkinformatie= ec2.describe_vpcs()
        elinformatie = ec2.describe_addresses()
        #print(instanceinformatie['Reservations'])

        instanceinformationlist.append(regio)
        #deze regel is om de vpc te printen
        for value1 in range (0,len(netwerkinformatie['Vpcs'])):
            nwinfo=netwerkinformatie['Vpcs'][value1]['VpcId'],netwerkinformatie['Vpcs'][value1]['CidrBlock']
            instanceinformationlist.append(nwinfo)

        #dit stukje is voor het printen van de elastic ip address
        #print(len(netwerkinformatie["Addresses"]))
        for value2 in range (0,len(elinformatie["Addresses"])):
            if len(elinformatie["Addresses"][value2]) < 10:
                elinfo=('deze elastic ip', elinformatie["Addresses"][value2]['PublicIp'],'is nergens mee verbonden')
                instanceinformationlist.append(elinfo)
            else:
                elinfo=('deze elastic ip',elinformatie["Addresses"][value2]['PublicIp'] ,'is verbonden met de instance',elinformatie["Addresses"][value2]['InstanceId'])
                instanceinformationlist.append((elinfo))

        #dit stukje hieronder is om de instances te checken
        if instanceinformatie['Reservations']==[]:
            instanceinformationlist.append(': geen ec2 instances in deze regio')
            continue

        #print(len(instanceinformatie))
        #print(instanceinformatie)
        for value in range(0,len(instanceinformatie['Reservations'])):
            #print(len(instanceinformatie),'dit is de lengte van in')

            #print('dit is de value',value)
            id = instanceinformatie['Reservations'][value]['Instances'][0]['InstanceId']
            instancetype=instanceinformatie['Reservations'][value]['Instances'][0]['InstanceType']
            status=instanceinformatie['Reservations'][value]['Instances'][0]['State']['Name']
            # naam=instanceinformatie['Reservations'][value]['Instances'][0]['Tags'][0]['Value']
            info=(id,instancetype,status)
            instanceinformationlist.append(info)

            #print(counter)
    return instanceinformationlist



def customkeylistalleinstances(regios,ACCESS_KEY,SECRET_KEY):
    instanceinformationlist=[]
    for regio in regios:
        lijstvanelasticaddresses = []
        my_config = Config(
            region_name=regio,
            signature_version='v4',

            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=my_config
        )
        instanceinformatie = ec2.describe_instances()
        netwerkinformatie= ec2.describe_vpcs()
        elinformatie = ec2.describe_addresses()
        #print(instanceinformatie['Reservations'])

        instanceinformationlist.append(regio)
        #deze regel is om de vpc te printen
        for value1 in range (0,len(netwerkinformatie['Vpcs'])):
            nwinfo=netwerkinformatie['Vpcs'][value1]['VpcId'],netwerkinformatie['Vpcs'][value1]['CidrBlock']
            instanceinformationlist.append(nwinfo)
        #dit stukje is voor het printen van de elastic ip address
        #print(len(netwerkinformatie["Addresses"]))
        for value2 in range (0,len(elinformatie["Addresses"])):
            if len(elinformatie["Addresses"][value2]) < 10:
                elinfo=('deze elastic ip', elinformatie["Addresses"][value2]['PublicIp'],'is nergens mee verbonden')
                instanceinformationlist.append(elinfo)
            else:
                elinfo=('deze elastic ip',elinformatie["Addresses"][value2]['PublicIp'] ,'is verbonden met de instance',elinformatie["Addresses"][value2]['InstanceId'])
                instanceinformationlist.append((elinfo))

        #dit stukje hieronder is om de instances te checken
        if instanceinformatie['Reservations']==[]:
            instanceinformationlist.append(': geen ec2 instances in deze regio')
            continue

        #print(len(instanceinformatie))
        #print(instanceinformatie)
        for value in range(0,len(instanceinformatie['Reservations'])):
            #print(len(instanceinformatie),'dit is de lengte van in')

            #print('dit is de value',value)
            id = instanceinformatie['Reservations'][value]['Instances'][0]['InstanceId']
            instancetype=instanceinformatie['Reservations'][value]['Instances'][0]['InstanceType']
            status=instanceinformatie['Reservations'][value]['Instances'][0]['State']['Name']
            # naam=instanceinformatie['Reservations'][value]['Instances'][0]['Tags'][0]['Value']
            info=(id,instancetype,status)
            instanceinformationlist.append(info)

            #print(counter)
    return instanceinformationlist


def securitygroupdef(regios, ACCESS_KEY, SECRET_KEY):
    securitylist = []
    counter2=1
    print(regios)
    for regio in regios:
        lijstvanelasticaddresses = []
        my_config = Config(
            region_name=regio,
            signature_version='v4',

            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        security = boto3.client(
            'ec2',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=my_config
        )
        securityinformation = security.describe_security_groups()
        if not securityinformation['SecurityGroups']:
            print('deze regio is empty',regio)
            continue

        securitylist.append(regio)
        securitylist.append([])



        securitygroupdict={}
        #print(regio)
        counter=1
        if (len(securityinformation['SecurityGroups'])) ==0:
            counter2+=2
            continue

        for y in range(len(securityinformation['SecurityGroups'])):
            groupid=(securityinformation['SecurityGroups'][y]['GroupId'])
            #print(groupid)

            securitylist[counter2].append(groupid)
            securitylist[counter2].append([])

            for x in range(len(securityinformation['SecurityGroups'][y]['IpPermissions'])):
                try:
                    if str((securityinformation['SecurityGroups'][y]['IpPermissions'][x]['IpProtocol']))== str(-1):
                        securitylist[counter2][counter].append('je hebt alle porten open')
                        continue
                except:
                    f='f'
                #print(range(len(securityinformation['SecurityGroups'][y]['IpPermissions'])))
                start=(securityinformation['SecurityGroups'][y]['IpPermissions'][x]['FromPort'])
                end=(securityinformation['SecurityGroups'][y]['IpPermissions'][x]['ToPort'])
                portrangelist=[]
                for x2 in range(start,end+1):

                    portrangelist.append(x2)

                #print('dit is de portrange',portrangelist)

                if 22 in portrangelist:
                    #print(range(len(securityinformation['SecurityGroups'][y]['IpPermissions'][x]['IpRanges'])))
                    for z in range(len(securityinformation['SecurityGroups'][y]['IpPermissions'][x]['IpRanges'])):
                        #print(securityinformation['SecurityGroups'][y]['IpPermissions'][x]['IpRanges'][z]['CidrIp'])
                        if securityinformation['SecurityGroups'][y]['IpPermissions'][x]['IpRanges'][z]['CidrIp']=='0.0.0.0/0':
                            #print('dit zijn de counters',counter2,counter)
                            #print('dit zijn de list items',securitylist[counter2])
                            securitylist[counter2][counter].append('je hebt de ssh port openstaan en iedereen kan erbij')

            counter+=2
        counter2+=2
    return securitylist

acces='AKIAREG27JVKSBWTSQGL'
password='nr9vE8EuRU5ku4Wi3IQThHS83GiNDH+NODnC72Pe'
#lijstvoorsecurityinformatie=(securitygroupdef(alleregios(),acces,password))
#print(lijstvoorsecurityinformatie)
#print(listalleinstances(alleregios()))
#print(alleregios()
# )


#lijstvoorsecurityinformatie = ['eu-north-1', [], 'ap-south-1', [], 'eu-west-3', [], 'eu-west-2', ['sg-0bf91dd38cb7592dd', ['je hebt alle porten open']], 'eu-west-1', ['sg-07a20d94e4aa7e988', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-09cfdc37ee1cc12f5', ['je hebt de ssh port openstaan en iedereen kan erbij', 'je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c971f51ea5349fc0', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0d76bb70a15bb6e3e', ['je hebt alle porten open'], 'sg-0e6d1fb3fd4379abd', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'ap-northeast-2', [], 'ap-northeast-1', [], 'sa-east-1', [], 'ca-central-1', [], 'ap-southeast-1', [], 'ap-southeast-2', [], 'eu-central-1', [], 'us-east-1', [], 'us-east-2', ['sg-082c29bb2634e0899', ['je hebt alle porten open']], 'us-west-1', ['sg-011a1be4cd070173c', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c17c80f13bbeb070', ['je hebt alle porten open'], 'sg-0d1a8a361826fa543', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'us-west-2', ['sg-0b14d3c4bc6a65896', ['je hebt alle porten open']], 'eu-north-1', [], 'ap-south-1', [], 'eu-west-3', [], 'eu-west-2', ['sg-0bf91dd38cb7592dd', ['je hebt alle porten open']], 'eu-west-1', ['sg-07a20d94e4aa7e988', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-09cfdc37ee1cc12f5', ['je hebt de ssh port openstaan en iedereen kan erbij', 'je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c971f51ea5349fc0', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0d76bb70a15bb6e3e', ['je hebt alle porten open'], 'sg-0e6d1fb3fd4379abd', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'ap-northeast-2', [], 'ap-northeast-1', [], 'sa-east-1', [], 'ca-central-1', [], 'ap-southeast-1', [], 'ap-southeast-2', [], 'eu-central-1', [], 'us-east-1', [], 'us-east-2', ['sg-082c29bb2634e0899', ['je hebt alle porten open']], 'us-west-1', ['sg-011a1be4cd070173c', ['je hebt de ssh port openstaan en iedereen kan erbij'], 'sg-0c17c80f13bbeb070', ['je hebt alle porten open'], 'sg-0d1a8a361826fa543', ['je hebt de ssh port openstaan en iedereen kan erbij']], 'us-west-2', ['sg-0b14d3c4bc6a65896', ['je hebt alle porten open']]]

#print(lijstvoorsecurityinformatie)

#print('dit is de lijst voor securityinformatie',lijstvoorsecurityinformatie)

def prinformation(lijstvoorsecurityinformatie):
    regiolist=[]
    grouplist=[]
    infolist=[]
    regiolist.append(len(lijstvoorsecurityinformatie))
    for x in range(0,len(lijstvoorsecurityinformatie),2):

        #print('regios',lijstvoorsecurityinformatie[x])
        for y in range(0,len(lijstvoorsecurityinformatie[x+1]),2):
            grouplist.append(len((lijstvoorsecurityinformatie[x+1])))
            #print(lijstvoorsecurityinformatie[x+1])
            #print('groep',lijstvoorsecurityinformatie[x+1][y])
            for z in range(0,len(lijstvoorsecurityinformatie[x+1][y+1]),2):
                #print(lijstvoorsecurityinformatie[x+1][y+1][z])
                infolist.append(len(lijstvoorsecurityinformatie[x+1][y+1]))
                #print(lijstvoorsecurityinformatie[x+1][y+1])

    return regiolist, grouplist, infolist
#print('dit is de securitylist')
#print(lijstvoorsecurityinformatie)

#regiolist,grouplist,infolist=prinformation(lijstvoorsecurityinformatie)
#print(regiolist, grouplist, infolist)
def printinformatie(lijstvoorsecurityinformatie,regiolist, grouplist, infolist):
    lengtofcounter=int(regiolist[0] / 2)
    for counter in range(0,lengtofcounter):
        for x2 in range(0,regiolist[0],2):
            print(lijstvoorsecurityinformatie[x2])

            for y2 in range(0,grouplist[counter],2):
                print(y2)
                print(lijstvoorsecurityinformatie[x2+1][y2])
                f='f'

                for z2 in range(0,infolist[counter],2):
                    #print(lijstvoorsecurityinformatie[x2+1][y2+1][z2])
                    f='f'

#print(prinformation(lijstvoorsecurityinformatie))
#print('dit is de test area voor printinformatie')
#printinformatie(lijstvoorsecurityinformatie,regiolist,grouplist,infolist)

