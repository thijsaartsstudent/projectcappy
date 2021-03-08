import boto3
from botocore.config import Config
ec2 = boto3.client('ec2')
response = ec2.describe_instances(region='us-west-1')
print(response)