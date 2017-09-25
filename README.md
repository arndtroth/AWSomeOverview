# AWSomeOverview.py

AWSomeOverview.py (speak: "awsome overview" or "Ooh, some overview!") is a script that iterates across multiple given AWS accounts, AWS regions and AWS services to aggregate and output facts.
It can be used to quickly get an overview or compare settings. It does not change any AWS resources, it is meant for plain read-only usage.
You can also generate outputs/documentation in different formats about the resources you have defined in an AWS environment. One of the possible output formats is the wiki table syntax.
As it is modular you can quickly add very simple plugins to combine the facts you are interested in. Thus AWSomeOverview.py can be used to check for compliance or company specific rule-sets.

Why not use aws-cli?
While you certainly can do most information retrieval with aws-cli (and sure we do use it everyday ourselves), AWSomeOverview.py will not limit you on:
- iterating through multiple AWS accounts (e.g.: -P $profile1,$profile2) 
- getting all attributes that are available through boto3
- combining facts from different API endpoints in one output (e.g.: -p elb,as,ec2 -r eu-west-1,us-east-1)
- defining additional outputs (beyond text,table,json)


# History and background

AWSomeOverview.py originated as an idea in 2014.
Our System Engineering team was working with a lot of AWS services spread across AWS accounts. The need to get a quick overview across AWS regions and the usage of AWS offerings became evident.
We also wanted to standardize output and reduce the time we spent with manually aggregating facts for documentation (JIRA tickets, wiki etc.).

# Setup

At the moment it needs to run in an virtual environment, which needs a bit of setup:

    virtualenv myenv
    source myenv/bin/activate
    pip install -r requirements.txt


# Credentials

AWSomeOverview.py uses boto3 internally, so you will need to pass a pair of AWS access keys.
To work with multiple profiles AWSomeOverview.py reads ~/.aws/config and prints the profiles found for selection.

# Invocation

    ./AWSomeOverview.py     // for help
    ./AWSomeOverview.py -h  // for help
    ./AWSomeOverview.py -a  // runs all plugins in all regions - the full matrix

It will generate a lot of output, and you can just copy/paste different sections into your wiki, while in raw edit mode.

We encourage you to use it to retrieve specific output, like:

    ./AWSomeOverview.py -p iam
    ./AWSomeOverview.py -p elb -r eu-west-1
    ./AWSomeOverview.py -p elb,as,ec2 -r eu-west-1,us-east-1
    ./AWSomeOverview.py -P AWS-profile1,AWS-profile2 -p elb,as,ec2 -r eu-west-1,us-east-1


# Known issues

- ./AWSomeOverview.py -p iam,r53  do not like regions to be specified

# Maintainers

 Arndt Roth, Emil Filipov

Welcoming your feedback.

