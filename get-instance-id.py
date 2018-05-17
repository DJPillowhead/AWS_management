import argparse
import boto3

parser = argparse.ArgumentParser(
    description="A useful tool to "
    "get Instance IDs for EC2 instances knowing their name,"
    "or list all instances in a VPC.")
parser.add_argument(
    '-name', nargs=1, required=False,
    help="The name of the instance you want to query.")
parser.add_argument(
    '-vpc', nargs=1, required=True,
    help="The name of the VPC your instance is in."
    "If you don't know the vpc id, use list-vpcs.py.")
parser.add_argument(
    '-action', nargs=1, required=True,
    choices=['QUERY', 'LISTALL'],
    help="LIST if you want to list all instances in a VPC, "
    "or QUERY if you want to get the id of an instance knowing its name."
    "LISTALL lists all instances - even the ones without a name.")
args = parser.parse_args()

ec2 = boto3.resource('ec2')
vpc = ec2.Vpc(args.vpc[0])


def get_instance_id_by_name(instance_name):
    instance_ids = []
    for ec2_instance in vpc.instances.all():
        if ec2_instance.tags:
            for tag in ec2_instance.tags:
                if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                    instance_ids.append(ec2_instance.instance_id)
    return instance_ids


if args.action[0] == 'QUERY':
    if args.name:
        print(get_instance_id_by_name(args.name[0]))
    else:
        print("QUERY is only possible with adding the -name parameter too.")

elif args.action[0] == 'LISTALL':
    for i in vpc.instances.all():
        if i.tags:
            for tag in i.tags:
                if tag['Key'] == 'Name':
                    print(
                        "Name: ", tag['Value'], " Instance id: ",
                        i.instance_id)
