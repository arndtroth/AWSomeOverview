"""
Class for Data Extraction of Autoscaling information
"""
import boto3
from deplugins.base import AWSFact


class AutoScalingGroups(AWSFact):
    NAME = 'AutoscalingGroup'
    OPTION = 'as'

    ORDERED_HEADINGS = [
        'VPC', 'AZ', 'Name', 'Created', 'LBs', 'Min Size', 'Max Size']

    def retrieve(self, conn):
        for element in conn.describe_auto_scaling_groups()['AutoScalingGroups']:
            item = {
                "Name": element['AutoScalingGroupName'],
                "VPC": element['VPCZoneIdentifier'] or 'N/A',
                'AZ': ','.join(sorted(element['AvailabilityZones'])),
                'Created': element['CreatedTime'],
                'Instances': ','.join(repr(i) for i in element['Instances']),
                'LBs':','.join(str(i) for i in element['LoadBalancerNames']),
                'Min Size': str(element['MinSize']),
                'Max Size': str(element['MaxSize']),
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('autoscaling', region_name=region)
        conn.region_name = region
        return conn
