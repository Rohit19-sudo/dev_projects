import json
import logging
import boto3
from botocore.exceptions import ClientError
import datetime


# Replace it with bucket for which presigned url needs to be generated
BUCKET_NAME = ''

def create_presigned_post(expiration=3600,context= None,event = None):
    """Generate a presigned URL S3 POST request to upload a file
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param context: Lambda context
    :param event: Event object which triggered lambda
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(
        Bucket = BUCKET_NAME,
        Key = event['filename'],
        ExpiresIn = expiration 
    )
    except ClientError as e:
        logging.error(e)
        return None

    
    current_datetime = datetime.datetime.now()

    ddb = boto3.resource('dynamodb')

    # Adding request details to audit table in DynamoDB
    try:
        db_response = ddb.Table('RequestsLog').put_item(
        Item = {
            'id': context.aws_request_id,
            'request_metadata': {'source':event['source'],
            'filename':event['filename'],
            "timestamp":str(current_datetime),
            "metadata":event['metadata']}

        })
    except ClientError as e:
        logging.error(e)
        return None


    # The response contains the presigned URL and required fields
    return response

def lambda_handler(event, context):

    data = json.loads(event['body'])
    response = create_presigned_post(context=context,event = data)

    return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response)
        }
