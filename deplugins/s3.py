"""
Class for Data Extraction of S3
"""

import boto3

from deplugins.base import AWSFact


class S3Buckets (AWSFact):
    NAME = 'S3'
    OPTION = 's3'

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        for bucket in boto3.resource('s3').buckets.all():
            item = {"Name": bucket.name, 'Created': bucket.creation_date}
            self.data.setdefault( 'N/A', []).append(item)

    def connect(self, region):
#        return S3Connection(
#            aws_access_key_id=self.aws_id,
#            aws_secret_access_key=self.aws_key
#        )
#        print "Creating connection ...."
        return
