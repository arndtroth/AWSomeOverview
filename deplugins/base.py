"""
Base class for Data Extraction plugins to inherit
"""

import boto3

class AWSFact (object):
    SKIP_REGIONS = ['us-gov-west-1', 'cn-north-1']
    # Name of the fact as presented to the user
    NAME = 'Generic AWS Fact'
    # Command-line plugin name that will enable this class
    OPTION = 'generic'
    # Column names, given in the proper importance order to be used by output
    # plugins
    ORDERED_HEADINGS = ['Name']

    def __init__(self, profile=None, regions=[]):
        """
        AWSFact is a base class for collecting facts.
        You can pass a profile and region list (e.g. ['us-east-2', 'eu-west-1']).

        If no regions are specified, the default is to get facts for
        everything but SKIP_REGIONS.
        """
        if profile:
            boto3.setup_default_session(profile_name=profile)

        if regions:
            # If we have an explicit region request, we ignore the SKIP_REGIONS list
            active_regions = [
                region for region in self.get_all_regions()
                if region in regions]
        else:
            # Otherwise we use everything but the SKIPPED REGIONS
            active_regions = [
                region for region in self.get_all_regions()
                if region not in self.SKIP_REGIONS]
        self.conn_pool = [self.connect(region) for region in active_regions]
        self.data = dict([(region, []) for region in active_regions])

    @staticmethod
    def get_all_regions():
        """
        Retrieve all regions as strings
        """
        # Hardcoding region name. Any would do for this method, but if it is
        # missing, then you always hit an error if default region is not in env
        conn = boto3.client('ec2', region_name='us-east-1')

        return [region['RegionName'] for region in conn.describe_regions()['Regions']]

    def connect(self, region, aws_key=None):
        raise NotImplementedError("Must be implemented by subclasses")

    def retrieve_loop(self):
        result = []
        for conn in self.conn_pool:
            result.append(self.retrieve(conn))
        return result

    def retrieve(self, conn):
        raise NotImplementedError("Must be implemented by subclasses")

    def banner(self):
        return ''
