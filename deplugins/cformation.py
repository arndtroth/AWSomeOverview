"""
Class for Data Extraction from CloudFormation
"""

import boto3
from deplugins.base import AWSFact


class CloudFormation (AWSFact):
    NAME = "CloudFormation"
    OPTION = 'cform'

    ORDERED_HEADINGS = [
        'Name',
        'Status',
        'Description',
        'Created',
        'Updated',
        'ID',
        'Resources'
    ]

    SKIP_STATUSES = ('DELETE_COMPLETE',)

    def retrieve(self, conn):

        for element in conn.list_stacks()['StackSummaries']:
            if element['StackStatus'] in self.SKIP_STATUSES:
                continue
            item = {
                "Name": element['StackName'],
                "Status": element['StackStatus'],
                "Description": element['TemplateDescription'],
                #"Updated": element['LastUpdatedTime'] or 'N/A',
                "Created": element['CreationTime'],
                "Updated": getattr(element, 'LastUpdatedTime', 'N/A')
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('cloudformation', region_name=region)
        conn.region_name = region
        return conn
