import boto3
import json
from datetime import datetime


def generate_blog_from_topic(blog_title:str)->str:
    client = boto3.client("bedrock-runtime",region_name='us-east-1')
    model_id = "mistral.mistral-large-2402-v1:0"

    formatted_prompt = f"<s>[INST] Generate a 150 lines blog on the topic {blog_title} [/INST]"

    payload ={
        "prompt":formatted_prompt,
        "max_tokens":512,
        "temperature":0.6
    }

    request = json.dumps(payload)

    try:
        response=client.invoke_model(modelId=model_id,body=request)
        model_response=json.loads(response['body'].read())
        generated_blog=model_response['outputs'][0]['text']
        print(generated_blog)
        return generated_blog

    except Exception as e:
        print(f"No blog generated Issue has been happend: {e}")


def save_blog_to_s3(bucket_name,generated_text,bucket_key_name):
    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(Bucket=bucket_name,Key=bucket_key_name,Body=generated_text)
        print("Successfully save the blog into the bucket.")
    except Exception as e:
        print(f"No blog save Issue has been happend: {e}")



def lambda_handler(event, context):
    event = json.loads(event['body'])
    blog_topic = event['blog_topic']
    generate_blog = generate_blog_from_topic(blog_title=blog_topic)
    if generate_blog:
        current_time = datetime.now().strftime('%H%M%S')
        s3_bucket_key=f"Blog-output/{current_time}.txt"
        s3_bucket_name="blogs-buckets-generation" 
        save_blog_to_s3(generated_text=generate_blog,bucket_name=s3_bucket_name,bucket_key_name=s3_bucket_key)
        return{
        "statusCode":200,
        "body":json.dumps({
            "message":"Blog generated successfully.",
            "s3_key":s3_bucket_key
        })
    }
    else:
        return{
            "statusCode":500,
            "body":json.dumps({
                "message":"blog-geration failed try it again."
            })
        }

    
