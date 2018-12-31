import boto3
import json
import sys

print('MUST BE RUN FROM ORGANIZATION MASTER ACCOUNT')

# get organization details
client = boto3.client('organizations')
count = 1

# Check permission for organizations
try:
    response = client.describe_organization()
except Exception as err:
    print(err)
    sys.exit("looks like you don't have access to organizations....", err)


# Check if all features are enabled.
orgFeatureSet = response['Organization']['FeatureSet']

print(f'Current Features set to: {orgFeatureSet}')

# check for all features enabled, if not enable them.
if orgFeatureSet != 'ALL':
    print('all features needs to be enabled...')
    try:
        response = client.enable_all_features()
    except Exception as err:
        print(err)
        sys.exit("looks like you don't have access to enable all features in organizations....")
    
# check for RAM access is enabled, if not enable them.
try:
    orgServices = client.list_aws_service_access_for_organization()
    for i in orgServices['EnabledServicePrincipals']:
        if i['ServicePrincipal'] == 'ram.amazonaws.com':
            count += 1

    # RAM not enabled in organizations
    if count <= 1:
        print('ram features not enabled...trying to turn on now...')
        try:
            response = client.enable_aws_service_access(ServicePrincipal='ram.amazonaws.com')
        except Exception as err:
            print(err)
            sys.exit("looks like you don't have access to enable RAM service in organizations....")

except Exception as err:
    print(err)
    sys.exit("looks like you're not running this script from master account in organizations....")


print('account all good, ready for cloudformation scripts')
