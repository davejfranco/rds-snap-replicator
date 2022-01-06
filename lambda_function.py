#!/usr/bin/env python
import os
import sys
import boto3
import logging

SOURCE_REGION='eu-west-1'
TARGET_REGION='eu-central-1'

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def connect(region: str, service: str='rds'):

    try:
        session = boto3.Session(region_name=region)
    except Exception as err:
        logger.exception(err)
        sys.exit(1)
    
    try:
        return session.client(service)
    except Exception as err:
        logger.exception(err)
        sys.exit(1)


def check_if_snap_exists(snap_name: str, region: str=TARGET_REGION) -> bool:

    client = connect(region)
    
    try:
        client.describe_db_snapshots(DBSnapshotIdentifier=snap_name)
        return True
    except Exception:
        return False

def get_newest_snapshot(db_name: str, region: str=SOURCE_REGION) -> str:
    
    client = connect(region)

    response = client.describe_db_snapshots(
        DBInstanceIdentifier=db_name,
        SnapshotType='automated'
    )
    return response['DBSnapshots'][-1]

def replicate(region: str = TARGET_REGION):

    snap = get_newest_snapshot(os.environ['DB'])
    if not check_if_snap_exists(snap['DBSnapshotIdentifier']):
        client = connect(region)
        try:
            client.copy_db_snapshot(
                SourceDBSnapshotIdentifier=snap['DBSnapshotArn'],
                TargetDBSnapshotIdentifier=snap['DBSnapshotIdentifier'].split(':')[1],
                KmsKeyId=os.environ['KMS_KEY_ARN'],
                CopyTags=True,
                SourceRegion=SOURCE_REGION
            )
            logger.info(f"Snapshot: {snap['DBSnapshotArn']} succesfully coppied to region: {TARGET_REGION}")
        except Exception as error:
            logger.exception(error)


def lambda_handler(event, context):
    
    try: 
        replicate()
    except Exception as error:
        logger.exception(error)
    
    return {
        'statusCode': 200
    }