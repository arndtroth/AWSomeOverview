"""
Class for Data Extraction of Route 53
"""

from copy import copy

import boto3
from deplugins.base import AWSFact


class Route53 (AWSFact):
    NAME = 'Route53'
    OPTION = 'r53'

    ORDERED_HEADINGS = [
        'Zone', 'Name', 'Type']#, 'TTL', 'Record', 'Identifier', 'Region']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        for zone in conn.list_hosted_zones_by_name()['HostedZones']:
            #item = {
            #    "Name": zone['Name'],
            #    'Id': zone['Id']
            #}
            #self.data.setdefault('N/A', []).append(item)

            base_item = {'Zone': zone['Name']}
            for rec in conn.list_resource_record_sets(HostedZoneId=zone['Id'])['ResourceRecordSets']:
                mid_item = copy(base_item)
                mid_item['Name'] = rec['Name']
                mid_item['Type'] = rec['Type']
                #mid_item['TTL'] = rec['TTL']

                #print mid_item['Name']
                #print mid_item['Type']

            self.data.setdefault(None, []).append(mid_item)

    def connect(self, region):
        conn = boto3.client('route53')

        return conn
