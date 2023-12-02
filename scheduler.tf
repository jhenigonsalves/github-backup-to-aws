resource "aws_scheduler_schedule" "github_backup" {
  name       = "github_backup"
  group_name = "default"

  flexible_time_window {
    mode                      = "FLEXIBLE"
    maximum_window_in_minutes = 60

  }

  schedule_expression = "cron(1 1 1 * ? *)"


  target {
    arn      = aws_lambda_function.github_backup.arn
    role_arn = aws_iam_role.scheduler_invoke_lambda_role.arn
  }
}
