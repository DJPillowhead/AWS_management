These are sample scripts that help you manage AWS from command line so you save time and can do batch tasks easier.

One example could be to run a stop script to stop your dev instance as you go home (and a start one when you arrive) so you save money for the company.

Prerequisites:
- some kind of access to the AWS console of Chemaxon
- Python3 installed
- boto3 package installed (http://boto3.readthedocs.io/en/latest/guide/quickstart.html)

The scripts usually have some kind of help. 

1. python-aws-test.py
Tests if your connection is set up correctly

2. unused-sec-groups.py
It is a sample script how to find security groups that are not used.
Based on it you can create other queries easily.

3. list-sec-group-ip-permissions.py
You can list security groups that doesn't have any ip restrictions.
Can be useful to find out if you've made any mistake when creating a new.
(No security groups should expose anything without ip restrictions apart from port 80 and 443.)

4. manage-instance.py
You can start an aws ec2 instance with it providing the name of it.

5. get-instance-id.py
You can get the instance id of an EC2 instance knowing its name.

6. list-vpcs.py
You can list all the vpcs in your amazon account.
