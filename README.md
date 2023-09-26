# github-backup-to-aws
This project is an automated backup to store all the github repostories from an account to an AWS bucket. It's probably a good idea to do the Terraform Tutorial first.

# Step1
* Create a local python script that fetches all the github repositories from a account (both private and public), zips it and upload it to an AWS S3 Bucket with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) package. You will need to read the [github public rest api documentation](https://docs.github.com/en/rest) to understand how to fetch this data from github. Later we will rewrite this script to fit into an AWS Lambda Function. When calling `boto3` inside your python script, you will need to provide AWS Programatic access keys from a user. **LOAD THOSE CREDENTIALS VIA Environment Variables using [python-dotenv](https://pypi.org/project/python-dotenv/)!!!** Dont EVER commit those credentials to github.

# Step 2
* Create an AWS IAM User with full access to s3 buckets and full access to lambda functions (we might need more access later). Generate programatic access keys for this user. We will need this programatic access to configure our Terraform project. 

# Step 3
* Create Terraform configuration to integrate this project to an AWS account. You will need to configure the following files:
  * `backend.tf`
  * `providers.tf`
* With those files configured, test locally if you cant perform a `$ terraform init` and `$ terraform plan` successfully.

# Step 4
* Create Github Actions to deploy our infrastructure automatically using gitflow.

# Step 5
* Create a lambda function (python code + infrastructure) and deploy it with terraform through the CI/CD Pipeline.
