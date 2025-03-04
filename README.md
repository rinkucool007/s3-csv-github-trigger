# s3-csv-github-trigger

Step-by-Step Guide with AWS Secrets Manager
#
Step 1: Create Secret in AWS Secrets Manager
#
Go to AWS Secrets Manager in the AWS Console
#
Click "Store a new secret"
#
Select:
#
Secret type: "Other type of secret"
#
Key/value pairs: Add
#
Key: github_token
#
Value: YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
#
Secret name: github-token-secret

Click "Next" and keep default settings

Click "Store"

Note the Secret ARN (e.g., arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:github-token-secret-XXXXXX)

Step 2: Update IAM Role Permissions
Go to IAM → Roles
Find lambda-s3-github-role (created earlier)
Attach policy:
#
Click "Add permissions" → "Create inline policy"
#
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
#
Name: SecretsManagerAccess
Click "Create policy"

#
Step 3: Update Lambda Function Code
Go to Lambda → Functions → s3-csv-github-trigger
Replace the code with:
#
Click "Deploy"
#
Step 4: Verify Layer Configuration
Ensure the requests layer is still attached (from previous steps)
If not, re-add it as described earlier
#
Step 5: Test the Function
In Lambda, click "Test"
Use the same test event:
```
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "your-unique-bucket-name"
        },
        "object": {
          "key": "test.csv"
        }
      }
    }
  ]
}
```
#
Run the test and check the output
Verify in CloudWatch Logs if there are any permission issues
#
Step 6: Validate Full Flow
Upload test.csv to your S3 bucket
Check Lambda execution logs in CloudWatch
Verify the GitHub Actions workflow runs
#
Key Changes
Added boto3 to interact with Secrets Manager
Created get_secret() function to retrieve the token
Removed hardcoded token and used the secret instead
Added IAM permissions for Secrets Manager access
#
Notes
Replace REGION in the IAM policy with your AWS region (e.g., us-east-1)
Update region_name in get_secret() to match your region
Ensure your GitHub workflow file exists in the repository
The secret is securely stored and retrieved at runtime
