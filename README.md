# github-backup-to-aws
This project is an automated backup to store all the github repostories from an account to an AWS bucket. It's probably a good idea to do the Terraform Tutorial first.

# Step1
* Create a python script that fetches all the github repositories from a account (both private and public) and zips it. We will need to upload this zipped file to an AWS S3 bucket later. You will need to read the [github public rest api documentation](https://docs.github.com/en/rest) to understand how to fetch this data.

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
