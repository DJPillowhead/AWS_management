import argparse
import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser(
    description="A useful tool to "
    "stop or start your AWS instances.")
parser.add_argument(
    '-action', nargs=1, required=True,
    choices=['START', 'STOP', 'QUERY'],
    help="Use START or STOP to manage your instance "
    "or QUERY to get the state of the instances.")
parser.add_argument(
    '-filename', nargs=1, required=False,
    help="List of Instance IDs to be handled in a file, "
    "one item per line.")
parser.add_argument(
    '-instance_id', nargs=1, required=False,
    help="Instance ID of the AWS EC2 instance")
parser.add_argument(
    '-instancename', nargs=1, required=False,
    help="Instance name of the AWS EC2 instance")
args = parser.parse_args()

ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
all_vpcs = ec2.describe_vpcs()


def get_all_vpc_ids():
    all_vpc_ids = []
    for vpc in all_vpcs['Vpcs']:
        all_vpc_ids.append(vpc["VpcId"])
    return(all_vpc_ids)


def get_instance_id_by_name(instance_name):
    instance_ids = []
    queryable_vpc_ids = get_all_vpc_ids()
    for queryable_vpc_id in queryable_vpc_ids:
        vpc = ec2_resource.Vpc(queryable_vpc_id)
        for ec2_instance in vpc.instances.all():
            if ec2_instance.tags:
                for tag in ec2_instance.tags:
                    if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                        instance_ids.append(ec2_instance.instance_id)
    return instance_ids


# Check if filename is given as an input
if args.filename:
    with open(args.filename[0]) as f:
        instance_ids = f.readlines()
        instance_ids = [x.strip() for x in instance_ids]
    print(
        "Parsing input file, these instances will be affected:",
        instance_ids)
elif args.instance_id:
    instance_ids = args.instance_id
    print(
        "No input file found, this instance will be affected:\n",
        instance_ids)
elif args.instancename:
    instance_ids = get_instance_id_by_name(args.instancename[0])
    print(
        "Name parameter was called, this ID will be affected:\n",
        instance_ids)
else:
    print(
        "Nor input file nor instance ID has been found. \n"
        "Please add one of them. \n"
        "You can get instance IDs if you know the name "
        "by using get-instance-id.py \n"
        "Exiting.")
    exit()

# Check action type and try starting instances
if args.action[0] == 'START':
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=instance_ids, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(
            InstanceIds=instance_ids, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Check action type and try stopping instances
elif args.action[0] == 'STOP':
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=instance_ids, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(
            InstanceIds=instance_ids, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

elif args.action[0] == 'QUERY':
    instance_statuses = ec2.describe_instance_status(InstanceIds=instance_ids)
    for instance_id in instance_statuses['InstanceStatuses']:
        print(instance_id['InstanceId'], " *** ", instance_id['InstanceState'])
