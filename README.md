## What is this?

Command-line utility to query s3 backed yum repositories for packages from any system not only from linux that has Yum installed


## Install
```
python setup.py install
```

### Install with virtualenv
```
virtualenv venv
. bin/venv/activate
python setup.py install
```

## Usage

### Find package 'testartifact-snapshot'
```
#setup your environment first
. ~/aws-config/dev.sh

scripts/find-package.py --env -r https://BUCKET_NAME.snapshots.s3.amazonaws.com/cent6/ -p testartifact-snapshot --debug
```

##Help
```
Usage:
    find-package.py --repourl=<repo-url> --package=<package-name>  [--env|--iam] [--debug] [--filter=<filter>]

Attributes:
    --repourl=<repourl> -r          Repository URL eg. https://BUCKET_NAME.s3.amazonaws.com/cent6/
    --package=<package-name> -p     Package name to search for
    --filter=<filter> -f            Search only this sqlite database [default: primary]
    --env                           Pull credentials from the environment
    --iam                           Use IAM policy (Instance Profile) to obtain credentials
    --debug                         Show more debug info
```




## But I have yum how is it any better?

Yum pulls too much data and it's slow, this  utility will pull only necessary data from 1 repo without a need to use plugins.





## TODO

* Tests
* Docs
* IAM support

## Ideas

* checksum verification with manifest (repomd.xml)
* cleanup scripts - duplicate detection


## Like it?

* let me know at michal+github@bicz.net