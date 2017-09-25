"""
Class for Data Extraction of VPC instances
"""

import boto3
from deplugins.base import AWSFact


class VPC (AWSFact):

    NAME = "VPC"
    OPTION = 'vpc'
    ORDERED_HEADINGS = [
        'VPC ID', "CIDR", 'VPC Name', 'AZ', 'Subnet ID'
    ]

    def retrieve(self, conn):
        for element in conn.vpcs.all():
            subnets = sorted(element.subnets.all(), key = lambda x: x.availability_zone[-1])
            name_tags = dict((t['Key'],t['Value']) for t in element.tags or [] if t['Key']=='Name')
            name = name_tags.get('Name', '')
#            for subnet in element.subnets.all():
            item = {
                'VPC ID': element.id,
                'CIDR': element.cidr_block,
                "VPC Name": name,
                # Subnet properties
                'AZ' : ','.join(s.availability_zone[-1] for s in subnets),
                'Subent ID': ','.join(s.id for s in subnets),
            }
            self.data[conn.region_name].append(item)


    def connect(self, region):
        ## EC2 connection takes a region object, rather than a string
        conn = boto3.resource('ec2', region_name=region)
        conn.region_name = region
        return conn
