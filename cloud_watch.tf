resource "aws_cloudwatch_log_group" "lambda_function_cloudwatch_log_group" {
  name              = "/aws/lambda/${local.lambda_github_backup.name}"
  retention_in_days = 90
  lifecycle {
    prevent_destroy = false
  }
}
