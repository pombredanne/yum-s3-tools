#!/usr/bin/env python
"""
Usage: 
    find-package.py --repourl=<repo-url> --package=<package-name>  [--env|--iam] [--debug] [--filter=<filter>]

Attributes:
    --repourl=<repourl> -r          Repository URL eg. https://BUCKET_NAME.s3.amazonaws.com/cent6/ 
    --package=<package-name> -p     Package name to search for
    --filter=<filter> -f            Search only this sqlite database [default: primary] 
    --env                           Pull credentials from the environment
    --iam                           Use IAM policy (Instance Profile) to obtain credentials
    --debug                         Show more debug info
"""


from yums3tools import S3YumRepo
import docopt

def main():
    arguments = docopt.docopt(__doc__)
    debug = arguments['--debug']
    if debug: 
        print arguments
    #repo_url should follow the format of 
    #repo_url='https://BUCKET_NAME.s3.amazonaws.com/cent6/'
    #hardcoding env auth for now
    repo_url = arguments['--repourl']
    package = arguments['--package']
    #default filter, look only for packages in 'primary' sqlite, overrideable
    filter = arguments['--filter']
    repo = S3YumRepo('env', repo_url, filter, debug)
    if package in repo.packages.keys():
        print "Package {0} found! Version: {1}".format(package, repo.packages[package]) 

if __name__ == '__main__':
    main()
