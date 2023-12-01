resource "aws_lambda_function" "github_backup" {
  filename         = local.lambda_github_backup.zip_file
  function_name    = "github_backup"
  role             = aws_iam_role.realtime_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  timeout          = var.lambda_timeout
  memory_size      = var.memory_size
  package_type     = var.package_type
  source_code_hash = data.archive_file.lambda_encounter_type_general_zip.output_base64sha256
  runtime          = var.runtime
  layers           = [aws_lambda_layer_version.psycopg2_pandas_layer.arn]

  depends_on = [
    aws_iam_role.realtime_lambda_role
  ]
}