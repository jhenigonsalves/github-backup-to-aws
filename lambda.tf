resource "aws_lambda_layer_version" "requests_ratelimit_layer" {
  s3_bucket  = "public-objects-31415"
  s3_key     = "lambda-layer/python.zip"
  layer_name = "requests_ratelimit_layer"

  compatible_runtimes = [var.runtime]
}


resource "aws_lambda_function" "github_backup" {
  filename         = local.lambda_github_backup.zip_file
  function_name    = local.lambda_github_backup.name
  role             = aws_iam_role.github_backup_lambda_function_role.arn
  handler          = "lambda_function.lambda_handler"
  timeout          = var.lambda_timeout
  memory_size      = var.memory_size
  package_type     = var.package_type
  source_code_hash = data.archive_file.lambda_github_backup_zip.output_base64sha256
  runtime          = var.runtime
  layers           = [aws_lambda_layer_version.requests_ratelimit_layer.arn]

  depends_on = [
    aws_iam_role.github_backup_lambda_function_role,
    aws_cloudwatch_log_group.lambda_function_cloudwatch_log_group
  ]
}
