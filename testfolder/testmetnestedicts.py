import boto3
from botocore.config import Config
ec2 = boto3.client('ec2')
response = ec2.describe_instances()


def customkeylistalleinstances(regios,ACCESS_KEY,SECRET_KEY):
    instanceinformationlist=[]
    counter2 = 1
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
        if not instanceinformatie["Reservations"]:
            print('deze regio is empty',regio)
            continue
        instanceinformationlist.append(regio)
        instanceinformationlist.append([])
        #print(instanceinformatie['Reservations'])
        counter = 1
        instanceinformationlist.append(regio)
        #deze regel is om de vpc te printen
        #for value1 in range (0,len(netwerkinformatie['Vpcs'])):
        #    nwinfo=netwerkinformatie['Vpcs'][value1]['VpcId'],netwerkinformatie['Vpcs'][value1]['CidrBlock']
        #    instanceinformationlist.append(nwinfo)
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
