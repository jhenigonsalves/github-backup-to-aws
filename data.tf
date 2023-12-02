data "archive_file" "lambda_github_backup_zip" {
  type        = "zip"
  source_file = "aux_files/lambda_function.py"
  output_path = local.lambda_github_backup.zip_file
}

data "aws_secretsmanager_secret" "github_backup" {
  arn = "arn:aws:secretsmanager:us-east-1:210242717093:secret:prod/github-backup-u7Ivlh"
}

data "aws_secretsmanager_secret_version" "backup_current" {
  secret_id = data.aws_secretsmanager_secret.github_backup.id
}
