# Overview

GitHub Backup to AWS is an automated solution designed to back up all GitHub repositories from an account to an AWS S3 bucket. The project uses Terraform for infrastructure provisioning, Python for script execution, and GitHub Actions for continuous integration and deployment. The architecture ensures a secure and efficient backup process.

## Get Started with the Project

1. Fork Github Project
1. Add AWS credentials as a Secret on Github Project. The credentials must have enough privileges to make the deployment. So it need to be able to:
   * Read/Write to terraform bucket
   * Read the user created Secret from AWS Secrets Manager
   * Create AWS Lambda Functions
   * Create AWS Lambda Layers
   * Create AWS Cloud Watch Groups
   * Create AWS S3 Buckets
   * Create AWS IAM Roles
   * Create AWS EventBridge Scheduler

1. Create a bucket manually on AWS Account to hold the Terraform State. Turn on Versioning for this bucket and leave everything private.
1. Modify backup.tf: add your terraform state bucket at line 4

1. Create a Secret on AWS Secrets Manager (explain what fields must be there)

   * The secret must be called:
      <div style='text-align: center;'>
        prod/github-backup/
      </div>

   * The secret must contain the pairs key/value:
  
    | Key | Value | Description
    | :------: | ----------- |:-----: |
    |TOKEN_GITHUB | foo string | Personal token to access user authenticated content from GitHub [Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
    | BACKUP_ONLY_OWNER_REPOS | True \| False | Define which repos to download. If only the ones that user is owner or colaborator too.|True \| False
    | BACKUP_S3_BUCKET | my-backup-s3-bucket | S3 bucket name |
    | BACKUP_S3_PREFIX| 'my-prefix' | the name of the prefix inside the bucket where you should put the files

1. Modify locals.tf: add your secret arn at line 9

1. Commit and push the modifications. After a push/merge to the master branch the deploy will occur automatically.

## A Closer Look at Terraform's Provisioned Resources

Terraform will use the *aws provider* to create a few AWS recurses:

1. Two IAM Roles (aws_iam_role)
   * github_backup_lambda_function_role: This role allows the lambda function to:
     1. list all s3 buckets
     2. PutObject, ListBucket and GetBucketPolicy in the bucket defined on AWS Secret
     3. list all secrets on AWS Secrets Manager
     4. GetSecretValue and DescribeSecret in the secret declared at locals.tf
   * scheduler_invoke_lambda_role: This role allows the Event Bridge Scheduler to:
     1. Invoke Lambda Function
2. One Lambda Function with a lambda layer
   * requests_ratelimit_layer: The lambda layer will be created with a zip file located at a public s3 bucket. And it's needed because the lambda layes uses the *requests* and *ratelimit* python's library which are not native. The jutificative to use ratelimit is below in the topic "Why a Lambda Layer is necessary"
   * The Lambda Function that does all the work of getting the GitHub's repositories
3. One S3 bucket:
   * The bucket defined at the key: *BACKUP_S3_BUCKET* of the secret *prod/github-backup/*
   * The bucket that will store all the backups from github.
4. One CloudWatch Group
   * The log group that will keep the logs from the lambda fucntion runtime
5. One EventBridge Scheduler
   * The scheduler that will trigger the lambda function every 1st day of the month.

The overall architecture is as follows:
![architecture](diagrams/github-backup.png)

## Why a Lambda Layer is necessary

  Describe that was necessary to use rate limit not to overload Githubs Public API.

* Describe your unit tests for logic code
* Describe CI/CD with Github Actions
