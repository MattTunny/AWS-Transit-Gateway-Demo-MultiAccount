# AWS Transit GateWay Demo with Session Manager between Multi Accounts
These cloudformation templates will create a VPC with Transit Gatway and share it between 2 accounts. SSM is already configured so its easy to test network connectivity.

![](https://github.com/MattTunny/AWS-Transit-Gateway-Demo-MultiAccount/blob/master/tgw1.jpg)
<br>

## Pre-reqs
- Organizations needs to be abled with ALL features turn on (run python script 'enable-all-features.py' to enable)
- 2 AWS Accounts.
- 1 s3 bucket for zip files, Custom Lambda Resources are required as cloudformation/lambda API havn't been updated to include TransitGateway or RAM yet.

## Demo
This will create everything for you, if you running cloudformation from the browser use seperate browsers so you can tab between.

* From Account 1 (Org Master), Copy the 2 zip files into you're s3 bucket (share-resources.zip & update-route-table.zip)

* Fill in the 2 Paramaters in 'account-1.yaml': s3 Bucket with zip files & 2nd AWS Account Id. Rest can be left as is

* Run Account-1.yaml cloudformation template

```
aws cloudformation package --s3-bucket randombucket --template-file account-1.yaml --output-template-file output1.yaml
aws cloudformation deploy --template-file output1.yaml --stack-name 'TransitDemo' --capabilities CAPABILITY_IAM
```

* Once Stack has completed, get the TransitGateWay Output from Cloudformation (TransitGateWay Id) and add it to Paramater in 'account-2.yaml'

* Run Account-2.yaml cloudformation template for account-2

```
aws cloudformation package --s3-bucket randombucket --template-file account-2.yaml --output-template-file output2.yaml --profile account2
aws cloudformation deploy --template-file output2.yaml --stack-name 'TransitDemo' --capabilities CAPABILITY_IAM --profile account2
```

* You should now have connectivity between 2 accounts. SSM Session Manager is configured in this template so if you have upgraded SSM agent installed locally you can test:

```
aws ssm start-session --target 'i-09dd3dd5b22d7f123'
```

## Cleanup
Remember to delete the stacks when finished

```
aws cloudformation delete-stack --stack-name 'TransitDemo'
aws cloudformation delete-stack --stack-name 'TransitDemo' --profile account2
```
