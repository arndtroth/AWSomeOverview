"""
Class for Data Extraction from CloudFront
"""

import boto3

from deplugins.base import AWSFact


class CloudFront (AWSFact):

    NAME = "CloudFront-SSL"
    OPTION = 'cfront_ssl'

    ORDERED_HEADINGS = ['Id', 'SSLSupportMethod', 'MinimumProtocolVersion', 'IAMCertificateId']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        #for element in conn.list_distributions()['DistributionList']['Items']:
        for element in conn.list_distributions().get('DistributionList',{}).get('Items',[]):
            item = {
                "Id": element['Id'],
                "SSLSupportMethod": element['ViewerCertificate']['SSLSupportMethod'],
                "MinimumProtocolVersion": element['ViewerCertificate']['MinimumProtocolVersion'],
                "IAMCertificateId": element['ViewerCertificate']['IAMCertificateId'],
            }
            self.data.setdefault('N/A', []).append(item)

    def connect(self, region):
        conn = boto3.client('cloudfront', region_name=region)
        conn.region_name = region
        return conn
