# github-backup-to-aws
This project is an automated backup to store all the github repostories from an account to an AWS bucket. It's probably a good idea to do the Terraform Tutorial first. The architecture looks like this:
![architecture](diagrams/github-backup.png)

# Step 1
* Install `venv` to use a virtual environment on this project, when developing locally, it's important to create an isolate environment for each project so you can properly constrain the project dependencies. Take a look at [this guide to setup venv](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-20-04-quickstart) and create a `venv` called `venv`.
* Always remember to activate this `venv` before developing your python code for this project.
* The `venv` folder should live at the root of this github project.


# Step 2
* Create a local python script that fetches all the github repositories from a account (both private and public), zips it and upload it to an AWS S3 Bucket with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) package. You will need to read the [github public rest api documentation](https://docs.github.com/en/rest) to understand how to fetch this data from github. Later we will rewrite this script to fit into an AWS Lambda Function. When calling `boto3` inside your python script, you will need to provide AWS Programatic access keys from a user. **LOAD THOSE CREDENTIALS VIA Environment Variables using [python-dotenv](https://pypi.org/project/python-dotenv/)!!!** Dont EVER commit those credentials to github.


# Step 3
* Create a python package containin your lambda code, so you can distribute it easily to other python projectcs (This will be important when start creating our test suite). Read this about [setup.py](https://www.geeksforgeeks.org/what-is-setup-py-in-python/) to build your package. Once you have it configure, just run `$ pip install -e .` on your virtual environment.


# Step 4
* Decompose the python script on `Step2` into a python AWS Lambda Function. Modularize any custom logic in python function so we can test them easily.
* After decomposing the python script into a modularized lambda, create a test suit to test you code using [pytest](https://docs.pytest.org/en/7.4.x/). Your test suit will need to find the path of your lambda code, for


# Step 5
* Create an AWS IAM User with full access to s3 buckets and full access to lambda functions (we might need more access later). Generate programatic access keys for this user. We will need this programatic access to configure our Terraform project. 



# Step 6
* Create Terraform configuration to integrate this project to an AWS account. You will need to configure the following files:
  * `backend.tf`
  * `providers.tf`
* With those files configured, test locally if you cant perform a `$ terraform init` and `$ terraform plan` successfully. (you can deploy an anamazon S3 bucket to test if this is working via Terraform)


# Step 7
* Create Github Actions to deploy our infrastructure automatically using [Gitflow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow).
![architecture](diagrams/gitflow-simplified.png)

# Step 8
* Create a lambda function (python code + infrastructure) and deploy it with terraform through the CI/CD Pipeline using [Github Actions](https://docs.github.com/en/actions).
