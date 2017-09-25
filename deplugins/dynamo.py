"""
Class for Data Extraction from Dynamo DB
"""

import boto3
from deplugins.base import AWSFact


class DynamoDB (AWSFact):
    NAME = "DynamoDB"
    OPTION = 'dynamo'

    ORDERED_HEADINGS = [
        'Name',
        'Status',
        'Size',
        'ReadCU',
        'WriteCU',
        'Created',
        'ARN'
    ]

    def retrieve(self, conn):

        for table in conn.list_tables()['TableNames']:
            element = conn.describe_table(TableName=table)['Table']
            item = {
                "Name": element['TableName'],
                "Status": element['TableStatus'],
                "Size": element['TableSizeBytes'],
                "ReadCU": element['ProvisionedThroughput']['ReadCapacityUnits'],
                "WriteCU": element['ProvisionedThroughput']['WriteCapacityUnits'],
                "Created": element['CreationDateTime'],
                "ARN": element['TableArn']
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('dynamodb', region_name=region)
        conn.region_name = region
        return conn