"""
Class for Data Extraction from CloudWatch"""

import boto3
from deplugins.base import AWSFact


class CloudWatch (AWSFact):
    NAME = "CloudWatch"
    OPTION = 'cwatch'

    ORDERED_HEADINGS = [

        'Alarmname',
        'ActionsEnabled',
        'Action',
        'Status',
        'Updated',
        'Resources'
    ]

    def retrieve(self, conn):

        print "\n++++++++++++++++++++++++++++++++++++++++++++\n"
        print "      Showing all alarms found!"
        print "\n++++++++++++++++++++++++++++++++++++++++++++\n"

        for element in conn.describe_alarms()['MetricAlarms']:
            item = {
                "Alarmname": element['AlarmName'],
                "ActionsEnabled": element['ActionsEnabled'],
                "Action": ', '.join(element['AlarmActions']),
                "Status": element['StateReason'],
                "Updated": element['StateUpdatedTimestamp']
            }
            self.data[conn.region_name].append(item)

    def connect(self, region):
        conn = boto3.client('cloudwatch', region_name=region)
        conn.region_name = region
        return conn