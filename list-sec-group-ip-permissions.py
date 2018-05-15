import boto3
# You should use the credential profile file
ec2 = boto3.client("ec2")

# In boto3, if you have more than 1000 entries,
# you need to handle the pagination
# using the NextToken parameter, which is not shown here.

all_sg = ec2.describe_security_groups()


for security_group in all_sg["SecurityGroups"]:
    for ipPermission in security_group["IpPermissions"]:
        for ipRange in ipPermission["IpRanges"]:
            if (ipRange["CidrIp"]) == "0.0.0.0/0":
                print(security_group["GroupName"])
