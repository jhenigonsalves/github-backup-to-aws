# Overview

GitHub Backup to AWS is an automated solution designed to back up all GitHub repositories from an account to an AWS S3 bucket. The project uses Terraform for infrastructure provisioning, Python for script execution, and GitHub Actions for continuous integration and deployment. The architecture ensures a secure and efficient backup process.

## Get Started - How to Use

1. Fork Github Project
1. Add AWS IAM credentials as Secrets on the forked Github Project (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`). The credentials must have enough privileges to make the deployment. So it need to be able to:
   * Read/Write to terraform bucket
   * Read the user created Secret from AWS Secrets Manager
   * Create AWS Lambda Functions
   * Create AWS Lambda Layers
   * Create AWS Cloud Watch Groups
   * Create AWS S3 Buckets
   * Create AWS IAM Roles
   * Create AWS EventBridge Scheduler

1. Create a bucket manually on AWS Account to hold the Terraform State. Turn on Versioning for this bucket and leave everything private.
1. Modify file **backup.tf**: add your terraform state bucket at line 4

1. Create a Secret on AWS Secrets Manager (explain what fields must be there)

   * The secret must be called: **prod/github-backup**

   * The secret must contain the pairs key/value:
  
    | Key | Value | Description
    | :------: | ----------- |:-----: |
    |TOKEN_GITHUB | foo string | Personal token to access user authenticated content from GitHub [Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
    | BACKUP_ONLY_OWNER_REPOS | True \| False | Define which repos to download. If only the ones that user is owner or colaborator too.|True \| False
    | BACKUP_S3_BUCKET | my-backup-s3-bucket | S3 bucket name |
    | BACKUP_S3_PREFIX| 'my-prefix' | the name of the prefix inside the bucket where you should put the files

1. Modify **locals.tf**: add your AWS Secrets Manager - Secret ARN at line 9

1. Commit and push the modifications. After a push/merge to the master branch the deploy will occur automatically via GithubActions (the template `terraform-apply` will be triggered).

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

GitHub's public API limits the number of requests that can be done whithin a time window. There are 3 kinds of ratelimits of interest to us:

1. The primary rate limit for authenticated users, which is 5000 requests per hour.
2. The primary rate limit for GITIHUB_TOKEN in GitHub Actions, which is 1000 requests per hour.
3. The secondary rate limit: *Make too many requests per minute. No more than 90 seconds of CPU time per 60 seconds of real time is allowed.*
  
If you want to know more about then you can access the [documentation](https://docs.github.com/pt/rest/overview/rate-limits-for-the-rest-api?apiVersion=2022-11-28)

For this reason wass necessary to use *limits* and  *sleep_and_retry* from the *ratelimit* python's library to garantee that no more than 30 calls are made per minute. As *ratelimit* and even *requests* are not native from AWS Lambda Runtime, it was necessary to create a layer that contains those dependencies.

## Unit Tests

## Describe CI/CD with Github Actions
