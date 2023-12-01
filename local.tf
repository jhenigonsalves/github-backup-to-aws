locals {
  # Lambda Configuration
  lambda_github_backup = {
    name      = "github_backup"
    handler   = "lambda_function.lambda_handler"
    zip_file = "github_backup.zip"
  }
}