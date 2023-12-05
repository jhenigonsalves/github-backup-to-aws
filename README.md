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
  
1. Modify backup.tf: add your terraform state bucket at line 4

* Modify locals.tf: add your secret arn at line 9

* Describe that was necessary to use rate limit not to overload Githubs Public API.
* Describe all resources that Terraform creates
* Describe your unit tests for logic code
* Describe CI/CD with Github Actions
