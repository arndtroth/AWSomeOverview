"""
Class for Data Extraction of ELBs
"""

import boto3
from deplugins.base import AWSFact


class ElasticLoadBalancer (AWSFact):

    NAME = "ELB Attributes"
    OPTION = 'elb_attr'

    ORDERED_HEADINGS = ['ELB Name', 'ConnectionDraining','CrossZoneLoadBalancing','IdleTimeout', 'AccessLog']

    def retrieve(self, conn):
        for lb in conn.describe_load_balancers()['LoadBalancerDescriptions']:
            attributes = conn.describe_load_balancer_attributes(LoadBalancerName=lb['LoadBalancerName'])['LoadBalancerAttributes']
            #import pdb;
            #pdb.set_trace()
            item = {
                "ELB Name": lb['LoadBalancerName'],
                #"ELB Attributes": conn.describe_load_balancer_attributes(LoadBalancerName=lb['LoadBalancerName'])['LoadBalancerAttributes']
                "ConnectionDraining": attributes['ConnectionDraining']['Enabled'],
                "CrossZoneLoadBalancing":   attributes['CrossZoneLoadBalancing']['Enabled'],
                "IdleTimeout": attributes['ConnectionSettings']['IdleTimeout'],
                "AccessLog": attributes['AccessLog']['Enabled'],
            }
            self.data[conn.region_name].append(item)
        return

    def connect(self, region):
        conn = boto3.client('elb', region_name=region)
        conn.region_name = region
        return conn

