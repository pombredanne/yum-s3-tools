# What is this?

Command-line utility to query s3 backed yum repositories for packages from any system not only from linux that has Yum installed


# How does it work?

```
% ./yum-s3-verify.py -h
Usage:
    yum-s3-verify.py --repourl=<repo-url> --package=<package-name>  [--env|--iam] [--debug]

Attributes:
    --repourl=<repourl> -r      Package name to search for
    --package=<package-name> -p      Package name to search for
    --env                                 Pull credentials from the environment
    --iam                                 Use IAM policy (Instance Profile) to obtain credentials
    --debug                               Show more debug info
```

#Example
```
. ~/aws-config/dev.sh
/yum-s3-verify.py --env -r https://net.bicz.dev.snapshots.s3.amazonaws.com/cent6/ -p testartifact-snapshot
Package testartifact-snapshot found! Version: 0-14
```




# But I have yum how is it any better?

Yum pulls too much data and it's slow, this  utility will pull only necessary data from 1 repo without a need to use plugins.





# TODO

Tests
Docs
IAM
