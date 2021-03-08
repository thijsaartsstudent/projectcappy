import boto3
from botocore.config import Config
import os
#print(os.environ['HOME'])

ACCESS_KEY='AKIAREG27JVKSBWTSQGL'
SECRET_KEY='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'
my_config = Config(
    region_name = 'eu-west-1',
    signature_version = 'v4',

    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

client = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=my_config
)

response = client.describe_instances()
print(response)



