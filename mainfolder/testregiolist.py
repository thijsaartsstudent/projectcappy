import boto3
ec2 = boto3.client('ec2')
lijstvanregios2=[]
def alleregios():

    response2 = ec2.describe_regions()
    regionsresponse = (response2['Regions'])
    for x in regionsresponse:
        lijstvanregios2.append(x['RegionName'])
    return lijstvanregios2

print(alleregios())