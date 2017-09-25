"""
Class for Data Extraction from Dynamo DB Streams
"""

import boto3
from deplugins.base import AWSFact


class DynamoDB (AWSFact):
    NAME = "DynamoDB"
    OPTION = 'dynamo_streams'

    ORDERED_HEADINGS = [
        'Name',
        'Status',
        'Size',
        'Enabled',
        'ViewType',
        'LatestStreamLabel',
        'LatestStreamArn'
    ]

    def retrieve(self, conn):

        for table in conn.list_tables()['TableNames']:
            element = conn.describe_table(TableName=table)['Table']
            item = {
                "Name": element['TableName'],
                "Status": element['TableStatus'],
                "Size": element['TableSizeBytes'],
                "Enabled": element['StreamSpecification']['StreamEnabled'],
                "ViewType": element['StreamSpecification']['StreamViewType'],
                "LatestStreamLabel": element['LatestStreamLabel'],
                "LatestStreamArn": element['LatestStreamArn']
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('dynamodb', region_name=region)
        conn.region_name = region
        return conn