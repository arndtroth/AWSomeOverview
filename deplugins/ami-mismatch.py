"""
Class for Data Extraction from Autoscaling and EC2 APIs
Goal is to find out if we run EC2 instances in an ASG that
have not been launched with the AMI defined in the Launch Config
"""
import boto3
from deplugins.base import AWSFact

class AmiMismatch(AWSFact):
    NAME = 'ami-mismatch'
    OPTION = 'ami-mismatch'

    ORDERED_HEADINGS = [
        'LC Name','ASG','AMI','Instances','Mismatch']

    def retrieve(self, conn):
        # init dictionary
        ami_dict={}
        # fill dictionary with key - value :  LC names and LC AMIs
        for element in conn.describe_launch_configurations()['LaunchConfigurations']:
            ami_dict[element['LaunchConfigurationName']]=element['ImageId']

        # Loop through ASGs and look up the AMI used on each instance
        for asg in conn.describe_auto_scaling_groups()['AutoScalingGroups']:

            goodinstancelist = []
            mismatchlist = []

            conn2 = boto3.client('ec2', region_name=conn.region_name)

            for i in asg['Instances']:

                instance_ami = conn2.describe_instances(InstanceIds=[i['InstanceId']])['Reservations'][0]['Instances'][0]['ImageId']

                if instance_ami == ami_dict[asg['LaunchConfigurationName']]:
                    goodinstancelist.append(i['InstanceId'])
                else:
                    mismatchlist.append(i['InstanceId'])

            item = {
                "LC Name": asg['LaunchConfigurationName'],
                "ASG": asg['AutoScalingGroupName'],
                "AMI": ami_dict[asg['LaunchConfigurationName']],
                'Instances': goodinstancelist,
                'Mismatch': mismatchlist,

            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('autoscaling', region_name=region)
        conn.region_name = region
        return conn



