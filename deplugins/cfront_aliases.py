"""
Class for Data Extraction from CloudFront
"""

import boto3

from deplugins.base import AWSFact


class CloudFront (AWSFact):

    NAME = "CloudFront-Aliases"
    OPTION = 'cfront_aliases'

    ORDERED_HEADINGS = ['Id', 'Status', 'Aliases']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        #for element in conn.list_distributions()['DistributionList']['Items']:
        for element in conn.list_distributions().get('DistributionList',{}).get('Items',[]):
            item = {
                "Id": element['Id'],
                "Aliases": element['Aliases']['Items'],
                "Status": element['Status'],
            }
            self.data.setdefault('N/A', []).append(item)
            #print item

    def connect(self, region):
        conn = boto3.client('cloudfront', region_name=region)
        conn.region_name = region
        return conn
