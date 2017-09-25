"""
Class for Data Extraction of Tags
"""

import boto3
from deplugins.base import AWSFact


class TAGS (AWSFact):

    NAME = "TAGS"
    OPTION = 'tags'

    ORDERED_HEADINGS = ['Instance','TagName', 'TagValue']

    #def banner(self):
    #    return "\n++++++++++++++++++++++++++++++++++++++++++++\n"+\
    #"      Showing just EC2 instance tags!"+\
    #"\n++++++++++++++++++++++++++++++++++++++++++++\n"

    def retrieve(self, conn):
        for instance in conn.instances.all():
            for element in instance.tags:
                #import pdb; pdb.set_trace()
                item = {
                    "Instance": instance.id,
                    "TagName": element['Key'],
                    "TagValue": element['Value']
                }
                self.data[conn.region_name].append(item)
        return

    def connect(self, region):
        conn = boto3.resource('ec2', region_name=region)
        conn.region_name = region
        return conn


### gets tags from all resources: aws ec2 describe-tags --output  table
