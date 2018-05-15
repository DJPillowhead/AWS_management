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
args = parser.parse_args()

ec2 = boto3.client('ec2')

# Check if filename is given as an input
if args.filename:
    with open(args.filename[0]) as f:
        Instance_IDs = f.readlines()
        Instance_IDs = [x.strip() for x in Instance_IDs]
    print(
        "Parsing input file, these instances will be affected:",
        Instance_IDs)
elif args.instance_id:
    Instance_IDs = args.instance_id
    print(
        "No input file found, this instance will be affected:",
        Instance_IDs)
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
        ec2.start_instances(InstanceIds=Instance_IDs, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(
            InstanceIds=Instance_IDs, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Check action type and try stopping instances
elif args.action[0] == 'STOP':
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=Instance_IDs, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(
            InstanceIds=Instance_IDs, DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

elif args.action[0] == 'QUERY':
    InstanceStatuses = ec2.describe_instance_status(InstanceIds=Instance_IDs)
    for InstanceId in InstanceStatuses['InstanceStatuses']:
        print(InstanceId['InstanceId'], " *** ", InstanceId['InstanceState'])
