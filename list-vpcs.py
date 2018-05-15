import boto3

# A simple script that lists all the VPCs that 
# you have in your configured Amazon account

ec2 = boto3.client('ec2')
all_vpcs = ec2.describe_vpcs()

for vpc in all_vpcs['Vpcs']:
    print("VPC id: ", vpc['VpcId'])
    for tag in vpc['Tags']:
        if tag['Key'] == 'Name':
            print("VPC name: ", tag['Value'])
