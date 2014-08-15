#!/bin/env python
"""
Usage: 
    yum-s3-verify.py --bucket=<bucket-name> --package-name=<package-name>  [--env|--iam] [--debug] [-v]


Attributes:
    --bucket=<bucket-name> -b             Bucket name to scan
    --package-name=<package-name> -p      Package name to search for
    --env                                 Pull credentials from the environment
    --iam                                 Use IAM policy (Instance Profile) to obtain credentials
    --debug                               Show more debug info
"""



import boto
import boto.s3.connection
import os
import sys
import docopt

def get_creds_from_env():
    try:
        access_key = os.environ['AWS_ACCESS_KEY']
        secret_key = os.environ['AWS_SECRET_KEY']
        region = os.environ['AWS_REGION']
    except:
        print "Environment not set properly!"
        sys.exit(1)
    return (access_key, secret_key)


class s3yumrepo(object):
    def __init__(self, auth, baseurl):
        (access_key, secret_key) = get_creds_from_env()
        conn = boto.connect_s3(aws_access_key_id = access_key, aws_secret_access_key = secret_key)
        key = bucket.get_key('perl_poetry.pdf')
        key.get_contents_to_filename('/home/larry/documents/perl_poetry.pdf')
  

def main():
    arguments = docopt.docopt(__doc__)
    if arguments['--debug']:
        print arguments
    repo_url = arguments['--repourl']
    if arguments['--iam']:
        repo = s3ymrepo('iam', '') 
    if arguments['--env']:




if __name__ == '__main__':
    main()
