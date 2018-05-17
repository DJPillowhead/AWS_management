import argparse
import boto3

parser = argparse.ArgumentParser(
    description="A useful tool to "
    "check security group ip permissions.")
parser.add_argument(
    '-iprange', nargs=1, required=True,
    help="The ip range you want to query for")
args = parser.parse_args()

ec2 = boto3.client("ec2")

# In boto3, if you have more than 1000 entries,
# you need to handle the pagination
# using the NextToken parameter, which is not shown here.

all_sg = ec2.describe_security_groups()


for security_group in all_sg["SecurityGroups"]:
    for ipPermission in security_group["IpPermissions"]:
        for ipRange in ipPermission["IpRanges"]:
            if ipRange == "":
                print(
                    security_group["GroupName"],
                    "doesn't have any IP limitation.")
            elif (ipRange["CidrIp"]) == args.iprange[0]:
                print(
                    security_group["GroupName"],
                    " has ", args.iprange[0], " as IP limitation.")
