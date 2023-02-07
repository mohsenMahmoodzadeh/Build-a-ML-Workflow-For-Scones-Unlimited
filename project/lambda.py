# Lambda Function 01: serialize_data

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    key = event["s3_key"]
    bucket = "sagemaker-studio-552470182774-mg6y3ntpjfg"
    
    boto3.resource('s3').Bucket(bucket).download_file(key, '/tmp/image.png')
    
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())
        
    print("Event:", event.keys())

    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
            
        }
    }

# Lambda Function 02: classify_image

    
import json
import base64
import boto3

ENDPOINT = "image-classification-2023-01-21-20-01-47-563"

runtime = boto3.Session().client('sagemaker-runtime')

def lambda_handler(event, context):

    image = base64.b64decode(event["body"]["image_data"])
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT, 
        ContentType='application/x-image', 
        Body=image
    )
    
    inferences = response["Body"].read().decode('utf-8')
    
    event["inferences"] = inferences

    return {
        'statusCode': 200,
        'body': {
            "inferences": json.loads(inferences)    
        }
    }
    

# Lambda Function 03: filter_confidence

import json

THRESHOLD = 0.85

def lambda_handler(event, context):
    
    inferences = event["body"]["inferences"]
    
    meets_threshold = max(inferences) > THRESHOLD
    
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }