import boto3
import json
import crhelper
import time
import os

# initialise logger
print('Loading function')
print('variables being passed....')

REGION = os.environ['REGION']
ACCOUNT = os.environ['ACCOUNT']
SECONDACC = os.environ['SECONDACC']
TRANSITGTW = os.environ['TRANSITGTW']
STACKNAME = os.environ['STACKNAME']

print(f'REGION = {REGION}')
print(f'ACCOUNT = {ACCOUNT}')
print(f'SECONDACC = {SECONDACC}')
print(f'TRANSITGTW = {TRANSITGTW}')
print(f'STACKNAME = {STACKNAME}')

logger = crhelper.log_config({"RequestId": "CONTAINER_INIT"})
logger.info('Logging configured')
# set global to track init failures
init_failed = False

try:
    # Place initialization code here
    logger.info("Container initialization completed")
except Exception as e:
    logger.error(e, exc_info=True)
    init_failed = e


def create(event, context):

    client = boto3.client('ram')
    b = client.create_resource_share(name=f'{STACKNAME}', resourceArns=[f'arn:aws:ec2:{REGION}:{ACCOUNT}:transit-gateway/{TRANSITGTW}'], principals=[f'{SECONDACC}'], allowExternalPrincipals=True)
    time.sleep(5)
    status = b['resourceShare']['status']
    response_data = {}
    response_data['ResourceShare'] = f'{status}'
    physical_resource_id = 'myResourceId'
    
    return physical_resource_id, response_data


def update(event, context):

    physical_resource_id = event['PhysicalResourceId']
    response_data = {}
    return physical_resource_id, response_data


def delete(event, context):

    client = boto3.client('ram')
    a = client.get_resource_shares(name=f'{STACKNAME}',resourceOwner='SELF')
    share = a['resourceShares'][0]['resourceShareArn']
    client.delete_resource_share(resourceShareArn=share)

    return


def handler(event, context):
    """
    Main handler function, passes off it's work to crhelper's cfn_handler
    """
    print('CloudFormation event received: %s' % str(event))
    # update the logger with event info
    global logger
    logger = crhelper.log_config(event)
    return crhelper.cfn_handler(event, context, create, update, delete, logger, init_failed)