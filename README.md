# s3-csv-github-trigger

Step-by-Step Guide with AWS Secrets Manager
#
Step 1: Create Secret in AWS Secrets Manager
#
Go to AWS Secrets Manager in the AWS Console
#
Click "Store a new secret"
Select:
Secret type: "Other type of secret"
Key/value pairs: Add
Key: github_token
Value: YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
Secret name: github-token-secret
Click "Next" and keep default settings
Click "Store"
Note the Secret ARN (e.g., arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:github-token-secret-XXXXXX)
Step 2: Update IAM Role Permissions
Go to IAM → Roles
Find lambda-s3-github-role (created earlier)
Attach policy:
Click "Add permissions" → "Create inline policy"
JSON:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:github-token-secret-XXXXXX"
        }
    ]
}
```
