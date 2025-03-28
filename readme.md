# DDNS Service

## Setup
1. Create A name record with your chosen subdomain
2. Create IAM policy like so: (fill in record name )
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "route53:GetChange",
                "route53:GetHostedZone",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringLike": {
                    "route53:ChangeResourceRecordSetsNormalizedRecordNames": [
                        "<domain name here>",
                        "*<domain name here>"
                    ]
                }
            }
        }
    ]
}
```
3. Create a IAM user and assign the above policy
4. Create an access key for the user
5. Pull the container, and fill environment variables
```
AWS_ACCESS_KEY=
AWS_ACCESS_SECRET=
A_RECORD_NAME=<RECORD_NAME>
HOSTED_ZONE_ID=
POLL_TIMEOUT_SECONDS=5
```