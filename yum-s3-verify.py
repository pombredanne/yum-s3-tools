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



#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
import boto
import os
import sys
import docopt
import tempfile
from xml import minidom

class Credentials(object):
    def __init__(self):
        pass
    @property
    def env(self):
        try:
            access_key = os.environ['AWS_ACCESS_KEY']
            secret_key = os.environ['AWS_SECRET_KEY']
            region = os.environ['AWS_REGION']
        except:
            print "Environment not set properly!"
            sys.exit(1)
        return (access_key, secret_key)
    def prompt(self):
        pass
    def iam(self):
        pass

class S3yumrepo(object):
    def __init__(self, auth, repo_url):
        creds = Credentials()
        (access_key, secret_key) = getattr(creds, auth)
        s3 = boto.connect_s3(aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        (self.repo_bucket_name, self.repo_path) = self.parse_s3_url(repo_url)
        self.bucket = s3.get_bucket(self.repo_bucket_name)
        self.repomd = bucket.get_key("{0}/repodata/repomd.xml".format(self.repo_path)).read()
        self.locations = self.repomd_locations(repomd)
        self.tmpdir = tempdir.mkdtemp()
        for location in locations:
            dest_filename = os.path.basename(location)
            sqlite_db = dest_filename.partition('.')[0]
            print "- Downloading {0}".format(sqlite_db)
            key = bucket.get_key(location)
            dest_path = "{0}/{1}".format(self.tmpdir, dest_filename)
            key.get_contents_to_filename(dest_path)
            setattr(self, sqlite_db, dest_path) 

    @property
    def packages(self):
        packages = {}
        primary_sqlite = bz2.BZ2File(self.primary) 
        primary_sqlite_uncompressed = tempfile.mktemp()
        with open(primary_sqlite_uncompressed, 'w') as p:
            p.write(primary_sqlite.read())

        sq = sqlite3.connect(primary_sqlite_uncompressed)   
        results = sq.execute("select * from packages")

        for (pkg, ver) in results:
            packages[pkg] = ver

        return packages

    def parse_s3_url(self, repo_url):
        #HACK: make it clear
        bucket_name = repo_url.partition('.s3')[0].replace('https://','').replace('http://','')
        path = repo_url.partition('.s3')[2].partition('/')[2]
        return (bucket_name, path)

    def repomd_locations(self, repomd):
        parsed = minidom.parseString(repomd)
        data = [ d for d in parsed.childNodes[0].childNodes if d.nodeType == 1 ]
        locations = [ l.childNodes[1].getAttribute('href') for l in data if l.childNodes[1].getAttribute('href') ]
        return locations

    def __del__(self):
        os.rmdir(self.tmpdir)

    
def main():
    arguments = docopt.docopt(__doc__)
    if arguments['--debug']:
        print arguments
    #repo_url should follow the format of 
    #repo_url='https://com.twilio.dev.packages.s3.amazonaws.com/cent6/'
    repo_url = arguments['--repourl']
    #hardcoding env auth for now
    repo = S3YumRepo('env', repo_url)

if __name__ == '__main__':
    main()
