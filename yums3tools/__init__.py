import boto
import os
import sys
import tempfile
from xml.dom import minidom
import bz2,sqlite3

class Credentials(object):
    def __init__(self):
        pass
    @property
    def env(self):
        try:
            access_key = os.environ['AWS_ACCESS_KEY']
            secret_key = os.environ['AWS_SECRET_KEY']
        except:
            print "Environment not set properly!"
            sys.exit(1)
        return (access_key, secret_key)
    def prompt(self):
        pass
    def iam(self):
        pass

class S3YumRepo(object):
    def __init__(self, auth, repo_url, filter, debug=False):
        creds = Credentials()
        (access_key, secret_key) = getattr(creds, auth)
        s3 = boto.connect_s3(aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
        (self.repo_bucket_name, self.repo_path) = self.parse_s3_url(repo_url)
        self.bucket = s3.get_bucket(self.repo_bucket_name)
        self.repomd = self.bucket.get_key("{0}/repodata/repomd.xml".format(self.repo_path)).read()
        self.filter = filter
        if debug: 
            print "Getting repomd" 
            print self.repomd
        self.locations = self.repomd_locations(self.repomd)
        if debug: 
            print "Locations"
            print self.locations
        self.tmpdir = tempfile.mkdtemp()
        if debug: 
            print "Using tmpdir"
            print self.tmpdir
        for location in self.locations:
            dest_filename = os.path.basename(location)
            sqlite_db = dest_filename.partition('.')[0]
            if self.filter: 
                if sqlite_db == self.filter:
                    if debug:
                        print "Processing {0}".format(location)
                else:
                    if debug:
                        print "Skipping {0}".format(location)
                    continue
            key = self.bucket.get_key("{0}/{1}".format(self.repo_path,location))
            if debug:
                print "key:{0}".format(key)
            dest_path = "{0}/{1}".format(self.tmpdir, dest_filename)
            key.get_contents_to_filename(dest_path)
            setattr(self, sqlite_db, dest_path) 

    @property
    def packages(self):
        """
        Returns a dictionary of packages.
        Key is package name
        Value is version of the package
        """
        packages = {}
        self.sqlite = {}
        with tempfile.NamedTemporaryFile() as u:
            with bz2.BZ2File(getattr(self,'primary')) as c:
                u.write(c.read())
            conn = sqlite3.connect(u.name)
            results = conn.execute("select * from packages")
            results = results.fetchall()
        for r in results:
            versions = ""
            version = "{0}-{1}".format(r[4],r[6])
            if packages.get(r):
                versions += version
            else:
                versions = version
            packages[r[2]]=versions
        return packages

    def parse_s3_url(self, repo_url):
        """
        Returns tupe of bucketname and path from http url
        """
        #HACK: make it clear
        bucket_name = repo_url.partition('.s3')[0].replace('https://','').replace('http://','')
        path = repo_url.partition('.s3')[2].partition('/')[2]
        return (bucket_name, path)

    def repomd_locations(self, repomd):
        """
        Extract locations from repomd.xml
        """
        parsed = minidom.parseString(repomd)
        data = [ d for d in parsed.childNodes[0].childNodes if d.nodeType == 1 ]
        locations = [ l.childNodes[1].getAttribute('href') for l in data if l.childNodes[1].getAttribute('href') ]
        return locations

def main():
    pass

if __name__ == '__main__':
    main()
