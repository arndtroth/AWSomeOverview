"""
Class for Data Extraction of EC2 instances
"""

import boto3
from deplugins.base import AWSFact


class EC2 (AWSFact):

    NAME = "EC2"
    OPTION = 'ec2'
    ORDERED_HEADINGS = [
        'AZ', 'VPC ID', 'ID', 'State', "Type", 'AMI', 'DevType',
        "EBS Optimized", 'Key Owner',
        "Public IP", "Private IP" 
    ]

    def retrieve(self, conn):
        for element in conn.instances.all():
            item = {
                'ID': element.id,
                #'Arch': element.architecture,
                "EBS Optimized": element.ebs_optimized,
                #"Security Groups": ', '.join(sorted(
                #    '%s (%s)' % (g.GroupName, g.GroupId) for g in element.security_groups)),
                #"Security Groups": element.security_groups,
                #"Block Devices": ', '.join(sorted(
                #    element.block_device_mappings)),
                #"Block Devices": element.block_device_mappings,
                "DevType": element.root_device_type,
                "EBS Optimized": element.ebs_optimized,
                "AMI": element.image_id,
                "Type": element.instance_type,
                "Public IP": element.public_ip_address,
                "Private IP": element.private_ip_address,
                "Key owner": element.key_name,
                'State': element.state['Name'],
                'AZ': element.placement['AvailabilityZone'],
                'VPC ID': element.vpc_id,
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.resource('ec2', region_name=region)
        conn.region_name = region
        return conn
