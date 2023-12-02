data "archive_file" "lambda_github_backup_zip" {
  type        = "zip"
  source_file = "aux_files/lambda_function.py"
  output_path = local.lambda_github_backup.zip_file
}
