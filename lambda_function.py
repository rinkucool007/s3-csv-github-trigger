import json
import urllib.parse
import requests
import boto3
import base64

def get_secret():
    secret_name = "github-token-secret"
    region_name = "us-east-1"  # Replace with your region
    
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)['github_token']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return json.loads(decoded_binary_secret.decode('utf-8'))['github_token']
    except Exception as e:
        raise e

def trigger_github_workflow(repo, workflow_id, token, ref, inputs):
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    payload = {'ref': ref}
    if inputs:
        payload['inputs'] = inputs
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.status_code

def lambda_handler(event, context):
    # Retrieve GitHub token from Secrets Manager
    github_token = get_secret()
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        if key.endswith('test.csv'):
            github_config = {
                'repo': 'your-username/your-repo',  # Replace with your repo
                'workflow_id': 's3-triggered-pipeline.yml',
                'token': github_token,
                'ref': 'main'
            }
            
            try:
                status = trigger_github_workflow(
                    github_config['repo'],
                    github_config['workflow_id'],
                    github_config['token'],
                    github_config['ref'],
                    {'bucket': bucket, 'file': key}
                )
                return {
                    'statusCode': 200,
                    'body': json.dumps(f'Workflow triggered successfully. Status: {status}')
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps(f'Error: {str(e)}')
                }
    
    return {
        'statusCode': 200,
        'body': json.dumps('No test.csv changes detected')
    }
