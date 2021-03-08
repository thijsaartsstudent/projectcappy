import boto3
from botocore.config import Config
ec2 = boto3.client('ec2')
response = ec2.describe_instances()
import datetime
from dateutil.tz import tzutc

def customkeylistalleinstances2(regios,ACCESS_KEY,SECRET_KEY,meetperformanceon,tijdverschil):
    fulldict={}
    instanceinformationlist=[]
    counter2 = 1
    for regio in regios:
        counter3=0
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

        try:
            ec2.describe_vpcs()
        except:
            return []
        netwerkinformatie = ec2.describe_vpcs()
        #test of hij empty is
        if not netwerkinformatie['Vpcs']:
            #print('deze regio is empty', regio)
            continue

        fulldict[regio] = {}
        fulldict[regio]['vpc'] = {}
        fulldict[regio]['elasticip'] = {}
        fulldict[regio]['gatewayid'] = {}


        instanceinformatie = ec2.describe_instances()
        elinformatie = ec2.describe_addresses()
        internetgateways=ec2.describe_internet_gateways()



        instanceinformationlist.append(regio)
        instanceinformationlist.append([])
        #print(instanceinformatie['Reservations'])
        counter = 1
        instanceinformationlist.append(regio)

        #deze regel is om de vpc te printen
        for value1 in range (0,len(netwerkinformatie['Vpcs'])):
            nwinfo1=netwerkinformatie['Vpcs'][value1]['VpcId']
            nwinfo2=netwerkinformatie['Vpcs'][value1]['CidrBlock']
            instanceinformationlist.append(nwinfo1)
            instanceinformationlist.append(nwinfo2)

            fulldict[regio]['vpc'][nwinfo1] = {}

            fulldict[regio]['vpc'][nwinfo1]['address'] = nwinfo1+' ' +nwinfo2
            #print(nwinfo1,nwinfo2,fulldict[regio]['vpc'][nwinfo1]['address'])

        #deze regels zijn voor internetgateways
        for value3 in range (0,len(internetgateways['InternetGateways'])):
            if not internetgateways['InternetGateways'][value3]['Attachments']:
                intergatewayvpcid = 'hij is niet attached'
                gatewayid = internetgateways['InternetGateways'][value3]['InternetGatewayId']

                fulldict[regio]['gatewayid'][gatewayid] = {}
                fulldict[regio]['gatewayid'][gatewayid]['intergatewayvpcid'] = intergatewayvpcid
                fulldict[regio]['gatewayid'][gatewayid]['information'] = gatewayid +' ' +intergatewayvpcid

            else:
                intergatewayvpcid= internetgateways['InternetGateways'][value3]['Attachments'][0]['VpcId']
                gatewayid=internetgateways['InternetGateways'][value3]['InternetGatewayId']
                gatewaystate=internetgateways['InternetGateways'][value3]['Attachments'][0]['State']

                fulldict[regio]['gatewayid'][gatewayid]={}
                fulldict[regio]['gatewayid'][gatewayid]['gatewaystate']=gatewaystate
                fulldict[regio]['gatewayid'][gatewayid]['intergatewayvpcid'] = intergatewayvpcid
                fulldict[regio]['gatewayid'][gatewayid]['information'] = gatewayid+' '+intergatewayvpcid

        #dit stukje is voor het printen van de elastic ip address
        #print(len(netwerkinformatie["Addresses"]))
        for value2 in range (0,len(elinformatie["Addresses"])):
            if len(elinformatie["Addresses"][value2]) < 10:
                elip = elinformatie["Addresses"][value2]['PublicIp']

                fulldict[regio]['elasticip'][elip] = {}
                fulldict[regio]['elasticip'][elip]['associated'] ='no'
                fulldict[regio]['elasticip'][elip]['information'] = elip+ ' association: '+ 'no'
                #print('deze elastic is niet verbonden',elip)
            else:

                verbondenmetinstance=elinformatie["Addresses"][value2]['InstanceId']
                elip = elinformatie["Addresses"][value2]['PublicIp']

                fulldict[regio]['elasticip'][elip] = {}
                fulldict[regio]['elasticip'][elip]['associated'] = verbondenmetinstance
                fulldict[regio]['elasticip'][elip]['information'] = elip+ ' association: '+ verbondenmetinstance

        #dit stukje hieronder is om de instances te checken
        #if instanceinformatie['Reservations']==[]:
        #    instanceinformationlist.append(': geen ec2 instances in deze regio')
        #    continue

        #print(len(instanceinformatie))
        #print(instanceinformatie)
        for value in range(0,len(instanceinformatie['Reservations'])):
            #print(len(instanceinformatie),'dit is de lengte van in')
            instancevpcid=instanceinformatie['Reservations'][value]['Instances'][0]['VpcId']
            #print('dit is de value',value)
            id = instanceinformatie['Reservations'][value]['Instances'][0]['InstanceId']
            instancetype=instanceinformatie['Reservations'][value]['Instances'][0]['InstanceType']
            status=instanceinformatie['Reservations'][value]['Instances'][0]['State']['Name']
            publicipaddress=instanceinformatie['Reservations'][value]['Instances'][0]['PrivateIpAddress']
            try:
                privateaddress=instanceinformatie['Reservations'][value]['Instances'][0]['PublicIpAddress']
            except:
                privateaddress=''
            # naam=instanceinformatie['Reservations'][value]['Instances'][0]['Tags'][0]['Value']
            info=(id,instancetype,status)
            instanceinformationlist.append(info)


            fulldict[regio]['vpc'][instancevpcid][id] = {}
            fulldict[regio]['vpc'][instancevpcid][id]['instancetype'] =instancetype

            fulldict[regio]['vpc'][instancevpcid][id]['status'] = status
            fulldict[regio]['vpc'][instancevpcid][id]['publicaddress'] = publicipaddress
            fulldict[regio]['vpc'][instancevpcid][id]['privateaddress'] = privateaddress
            if meetperformanceon ==1:
                performance=meetperformance(id,tijdverschil,ACCESS_KEY,SECRET_KEY,my_config)
                print(performance)
                fulldict[regio]['vpc'][instancevpcid][id]['status'] = status + ' '+performance

            #print(counter)
    return fulldict
lijstvanregios2=[]
def alleregios():

    response2 = ec2.describe_regions()
    regionsresponse = (response2['Regions'])
    for x in regionsresponse:
        lijstvanregios2.append(x['RegionName'])
    return lijstvanregios2


acces='AKIAREG27JVKSBWTSQGL'
password='nr9vE8EuRU5ku4Wi3IQThHS83GiNDH+NODnC72Pe'
#regios=['us-west-1','us-west-2','eu-west-1','eu-west-2']

ec2 = boto3.client('ec2')
response2 = ec2.describe_instances()
#print(response2)
cloudwatch=  boto3.client('cloudwatch')




periode=3600
def meetperformance(instanceid,tijdverschil,ACCESS_KEY,SECRET_KEY,my_config):
    cloudwatch = boto3.client('cloudwatch',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=my_config)
    endtime = datetime.datetime.now()
    starttime = endtime - datetime.timedelta(days=int(tijdverschil))
    print(endtime)
    print(starttime)
    lijstvoorperformanceavg=[]
    lijstvoorperformancemax=[]
    metricsresponsecpu= cloudwatch.get_metric_statistics(
        MetricName='CPUUtilization',
        StartTime=starttime,
        EndTime=endtime,
        Period=periode,
        Namespace='AWS/EC2',
        Statistics=['Maximum','Average'],
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },]
    )
    if not metricsresponsecpu['Datapoints']:
        print('deze is empty', metricsresponsecpu)
        return 'this instance is not used'
    else:
        for x in metricsresponsecpu['Datapoints']:
            lijstvoorperformanceavg.append(x['Average'])

        avgavg=sum(lijstvoorperformanceavg)/ len(lijstvoorperformanceavg)
        if avgavg <4:
            results='this instance is barely being used in the last '+str(tijdverschil)+"weeks the instance had a average cpu usage of"+str(avgavg)+'percent'
            return results




#print(meetperformance('i-0fa6ec3c1e3909de5',7,acces,password,))
#print('dit is de response')
#print(metricsresponse)


#antwoord=customkeylistalleinstances2(alleregios(),acces,password)


#print(type(antwoord['eu-west-1']['elasticip']['54.155.235.250']['information']))

#print(antwoord['eu-west-1']['vpc']['vpc-07d99d243ac4efaca'].keys())
#print(antwoord)
#print(metricsresponse['Datapoints'])
#for x in metricsresponsecpu['Datapoints']:
    #print(x['Maximum'])
#    if x['Maximum']> 20:
        #print(x)

rds = boto3.client('rds')
#resultaat=rds.describe_db_instances()
#print((resultaat))
import json

with open('test5.json') as f:
  data = json.load(f)

#print(data)
testdatabaseinformatie=data
#print(resultaat)
#testdatabaseinformatie={'DBInstances': [{'DBInstanceIdentifier': 'database-1-instance-1', 'DBInstanceClass': 'db.t2.small', 'Engine': 'aurora-mysql', 'DBInstanceStatus': 'available', 'MasterUsername': 'admin', 'Endpoint': {'Address': 'database-1-instance-1.cu03tq2d9mc8.eu-west-1.rds.amazonaws.com', 'Port': 3306, 'HostedZoneId': 'Z29XKXDKYMONMX'}, 'AllocatedStorage': 1, 'InstanceCreateTime': datetime.datetime(2021, 2, 23, 12, 29, 26, 752000, tzinfo=tzutc()), 'PreferredBackupWindow': '00:08-00:38', 'BackupRetentionPeriod': 1, 'DBSecurityGroups': [], 'VpcSecurityGroups': [{'VpcSecurityGroupId': 'sg-0d76bb70a15bb6e3e', 'Status': 'active'}], 'DBParameterGroups': [{'DBParameterGroupName': 'default.aurora-mysql5.7', 'ParameterApplyStatus': 'in-sync'}], 'AvailabilityZone': 'eu-west-1a', 'DBSubnetGroup': {'DBSubnetGroupName': 'default-vpc-07d99d243ac4efaca', 'DBSubnetGroupDescription': 'Created from the RDS Management Console', 'VpcId': 'vpc-07d99d243ac4efaca', 'SubnetGroupStatus': 'Complete', 'Subnets': [{'SubnetIdentifier': 'subnet-04e8881699a67924b', 'SubnetAvailabilityZone': {'Name': 'eu-west-1b'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}, {'SubnetIdentifier': 'subnet-00507a997adcdf50a', 'SubnetAvailabilityZone': {'Name': 'eu-west-1a'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}]}, 'PreferredMaintenanceWindow': 'wed:02:38-wed:03:08', 'PendingModifiedValues': {}, 'MultiAZ': False, 'EngineVersion': '5.7.mysql_aurora.2.07.2', 'AutoMinorVersionUpgrade': True, 'ReadReplicaDBInstanceIdentifiers': [], 'LicenseModel': 'general-public-license', 'OptionGroupMemberships': [{'OptionGroupName': 'default:aurora-mysql-5-7', 'Status': 'in-sync'}], 'PubliclyAccessible': False, 'StorageType': 'aurora', 'DbInstancePort': 0, 'DBClusterIdentifier': 'database-1', 'StorageEncrypted': True, 'KmsKeyId': 'arn:aws:kms:eu-west-1:077768641877:key/25ed50a4-e7fc-4acf-8971-a8bf8cb165dd', 'DbiResourceId': 'db-WU2S7XFZBIWFMG7ZFTYXBFCCGI', 'CACertificateIdentifier': 'rds-ca-2019', 'DomainMemberships': [], 'CopyTagsToSnapshot': False, 'MonitoringInterval': 60, 'EnhancedMonitoringResourceArn': 'arn:aws:logs:eu-west-1:077768641877:log-group:RDSOSMetrics:log-stream:db-WU2S7XFZBIWFMG7ZFTYXBFCCGI', 'MonitoringRoleArn': 'arn:aws:iam::077768641877:role/rds-monitoring-role', 'PromotionTier': 1, 'DBInstanceArn': 'arn:aws:rds:eu-west-1:077768641877:db:database-1-instance-1', 'IAMDatabaseAuthenticationEnabled': False, 'PerformanceInsightsEnabled': False, 'DeletionProtection': False, 'AssociatedRoles': [], 'TagList': [], 'CustomerOwnedIpEnabled': False}, {'DBInstanceIdentifier': 'database-2', 'DBInstanceClass': 'db.t3.micro', 'Engine': 'mysql', 'DBInstanceStatus': 'available', 'MasterUsername': 'admin', 'Endpoint': {'Address': 'database-2.cu03tq2d9mc8.eu-west-1.rds.amazonaws.com', 'Port': 3306, 'HostedZoneId': 'Z29XKXDKYMONMX'}, 'AllocatedStorage': 100, 'InstanceCreateTime': datetime.datetime(2021, 2, 23, 12, 34, 50, 520000, tzinfo=tzutc()), 'PreferredBackupWindow': '03:59-04:29', 'BackupRetentionPeriod': 7, 'DBSecurityGroups': [], 'VpcSecurityGroups': [{'VpcSecurityGroupId': 'sg-0d76bb70a15bb6e3e', 'Status': 'active'}], 'DBParameterGroups': [{'DBParameterGroupName': 'default.mysql8.0', 'ParameterApplyStatus': 'in-sync'}], 'AvailabilityZone': 'eu-west-1a', 'DBSubnetGroup': {'DBSubnetGroupName': 'default-vpc-07d99d243ac4efaca', 'DBSubnetGroupDescription': 'Created from the RDS Management Console', 'VpcId': 'vpc-07d99d243ac4efaca', 'SubnetGroupStatus': 'Complete', 'Subnets': [{'SubnetIdentifier': 'subnet-04e8881699a67924b', 'SubnetAvailabilityZone': {'Name': 'eu-west-1b'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}, {'SubnetIdentifier': 'subnet-00507a997adcdf50a', 'SubnetAvailabilityZone': {'Name': 'eu-west-1a'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}]}, 'PreferredMaintenanceWindow': 'wed:00:34-wed:01:04', 'PendingModifiedValues': {}, 'LatestRestorableTime': datetime.datetime(2021, 2, 23, 13, 20, tzinfo=tzutc()), 'MultiAZ': True, 'EngineVersion': '8.0.20', 'AutoMinorVersionUpgrade': True, 'ReadReplicaDBInstanceIdentifiers': ['testststst5'], 'LicenseModel': 'general-public-license', 'Iops': 3000, 'OptionGroupMemberships': [{'OptionGroupName': 'default:mysql-8-0', 'Status': 'in-sync'}], 'SecondaryAvailabilityZone': 'eu-west-1b', 'PubliclyAccessible': False, 'StorageType': 'io1', 'DbInstancePort': 0, 'StorageEncrypted': True, 'KmsKeyId': 'arn:aws:kms:eu-west-1:077768641877:key/25ed50a4-e7fc-4acf-8971-a8bf8cb165dd', 'DbiResourceId': 'db-EDPO4DBQR7RYY5TAWZB2OZMA34', 'CACertificateIdentifier': 'rds-ca-2019', 'DomainMemberships': [], 'CopyTagsToSnapshot': True, 'MonitoringInterval': 60, 'EnhancedMonitoringResourceArn': 'arn:aws:logs:eu-west-1:077768641877:log-group:RDSOSMetrics:log-stream:db-EDPO4DBQR7RYY5TAWZB2OZMA34', 'MonitoringRoleArn': 'arn:aws:iam::077768641877:role/rds-monitoring-role', 'DBInstanceArn': 'arn:aws:rds:eu-west-1:077768641877:db:database-2', 'IAMDatabaseAuthenticationEnabled': False, 'PerformanceInsightsEnabled': False, 'DeletionProtection': True, 'AssociatedRoles': [], 'MaxAllocatedStorage': 1000, 'TagList': [], 'CustomerOwnedIpEnabled': False}, {'DBInstanceIdentifier': 'testststst5', 'DBInstanceClass': 'db.t3.micro', 'Engine': 'mysql', 'DBInstanceStatus': 'available', 'MasterUsername': 'admin', 'Endpoint': {'Address': 'testststst5.cu03tq2d9mc8.eu-west-1.rds.amazonaws.com', 'Port': 3306, 'HostedZoneId': 'Z29XKXDKYMONMX'}, 'AllocatedStorage': 100, 'InstanceCreateTime': datetime.datetime(2021, 2, 23, 12, 56, 35, 181000, tzinfo=tzutc()), 'PreferredBackupWindow': '03:59-04:29', 'BackupRetentionPeriod': 0, 'DBSecurityGroups': [], 'VpcSecurityGroups': [{'VpcSecurityGroupId': 'sg-0d76bb70a15bb6e3e', 'Status': 'active'}], 'DBParameterGroups': [{'DBParameterGroupName': 'default.mysql8.0', 'ParameterApplyStatus': 'in-sync'}], 'AvailabilityZone': 'eu-west-1a', 'DBSubnetGroup': {'DBSubnetGroupName': 'default-vpc-07d99d243ac4efaca', 'DBSubnetGroupDescription': 'Created from the RDS Management Console', 'VpcId': 'vpc-07d99d243ac4efaca', 'SubnetGroupStatus': 'Complete', 'Subnets': [{'SubnetIdentifier': 'subnet-04e8881699a67924b', 'SubnetAvailabilityZone': {'Name': 'eu-west-1b'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}, {'SubnetIdentifier': 'subnet-00507a997adcdf50a', 'SubnetAvailabilityZone': {'Name': 'eu-west-1a'}, 'SubnetOutpost': {}, 'SubnetStatus': 'Active'}]}, 'PreferredMaintenanceWindow': 'wed:00:34-wed:01:04', 'PendingModifiedValues': {}, 'MultiAZ': False, 'EngineVersion': '8.0.20', 'AutoMinorVersionUpgrade': True, 'ReadReplicaSourceDBInstanceIdentifier': 'database-2', 'ReadReplicaDBInstanceIdentifiers': [], 'LicenseModel': 'general-public-license', 'Iops': 3000, 'OptionGroupMemberships': [{'OptionGroupName': 'default:mysql-8-0', 'Status': 'in-sync'}], 'PubliclyAccessible': False, 'StatusInfos': [{'StatusType': 'read replication', 'Normal': True, 'Status': 'replicating'}], 'StorageType': 'io1', 'DbInstancePort': 0, 'StorageEncrypted': True, 'KmsKeyId': 'arn:aws:kms:eu-west-1:077768641877:key/25ed50a4-e7fc-4acf-8971-a8bf8cb165dd', 'DbiResourceId': 'db-YENSPOT37EC36CNM7O3L32BEBI', 'CACertificateIdentifier': 'rds-ca-2019', 'DomainMemberships': [], 'CopyTagsToSnapshot': False, 'MonitoringInterval': 0, 'DBInstanceArn': 'arn:aws:rds:eu-west-1:077768641877:db:testststst5', 'IAMDatabaseAuthenticationEnabled': False, 'PerformanceInsightsEnabled': False, 'DeletionProtection': False, 'AssociatedRoles': [], 'MaxAllocatedStorage': 1000, 'TagList': [], 'CustomerOwnedIpEnabled': False}], 'ResponseMetadata': {'RequestId': 'cfd2ce34-ed21-4cf2-9ef0-6346a5fa88e1', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'cfd2ce34-ed21-4cf2-9ef0-6346a5fa88e1', 'content-type': 'text/xml', 'content-length': '13974', 'vary': 'accept-encoding', 'date': 'Tue, 23 Feb 2021 13:23:06 GMT'}, 'RetryAttempts': 0}}
#print(testdatabaseinformatie.keys())
dicfordatabases={}
dbinstance={}
dbcluster={}
#print(testdatabaseinformatie['DBInstances'][0])
for y in range(0,len(testdatabaseinformatie['DBInstances'])):
    #print(y)
    if testdatabaseinformatie['DBInstances'][y]['Engine']=='aurora-mysql':
        print()
        #deze regel is er voor te zorgen dat wanneer meerdere instances in dezelfde cluster zitten ze elkaar niet overschrijven
        if dbcluster == testdatabaseinformatie['DBInstances'][y]['DBClusterIdentifier']:
            print('true')
            dbinstance = testdatabaseinformatie['DBInstances'][y]['DBInstanceIdentifier']
            dicfordatabases[dbcluster][dbinstance] = {}
            continue
        dbcluster=testdatabaseinformatie['DBInstances'][y]['DBClusterIdentifier']
        #print(dbcluster)
        dbinstance=testdatabaseinformatie['DBInstances'][y]['DBInstanceIdentifier']
        dicfordatabases[dbcluster]={}
        dicfordatabases[dbcluster][dbinstance] = {}
    if testdatabaseinformatie['DBInstances'][y]['Engine'] == 'mysql':
        print()

print(dicfordatabases)