import boto3
import json
client = boto3.client('sns', endpoint_url='http://localhost:4566')
message = {"message": "Processing failed with error"}
try:
    response = client.publish(
        TargetArn="arn:aws:sns:us-east-1:000000000000:alpha-helix-ingestion-notification",
        Message=json.dumps({"email": json.dumps(message)}),
        Subject="File Registration: Error",
        #MessageStructure="json",
    )
    print(response)
except Exception as e:
    print(e)
