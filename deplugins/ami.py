"""
Class for Data Extraction of AMIs
"""

import boto3

from deplugins.base import AWSFact


class AMI (AWSFact):

    NAME = "AMI"
    OPTION = 'ami'
    ORDERED_HEADINGS = ['ID','RootDeviceType','DeleteOnTerm',
                        'DeviceName','Name','Description']

    def retrieve(self, conn):
        for element in conn.describe_images(DryRun=False,Owners=['self'])['Images']:

            #import pdb;pdb.set_trace()
            item = {
                "Name": element['Name'],
                'ID': element['ImageId'],
                'Description': element.get('Description',),
                #'DeviceName': element['BlockDeviceMappings'][0]['DeviceName'],
                'DeviceName': ','.join(str(i['DeviceName']) for i in sorted(element['BlockDeviceMappings'])),
                'RootDeviceType': element['RootDeviceType'],
                #'DeleteOnTerm': element['BlockDeviceMappings'][0].get('Ebs',{}).get('DeleteOnTermination','N/A'),
                'DeleteOnTerm': ','.join(str(i.get('Ebs',{}).get('DeleteOnTermination','N/A')) for i in sorted(element['BlockDeviceMappings'])),
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('ec2', region_name=region)
        conn.region_name = region
        return conn
