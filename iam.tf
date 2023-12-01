resource "aws_iam_role" "github_backup_lambda_function_role" {
  name = "github_backup_lambda_function_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonS3ObjectLambdaExecutionRolePolicy",
    ]

 inline_policy {
    name = "list_buckets_put_object"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Sid: "VisualEditor0",
          Action = [
				"s3:PutObject",
				"s3:ListBucket",
				"s3:GetBucketPolicy"
			],
          Effect = "Allow",
          Resource = "arn:aws:s3:::jheni-github-backup-bucket/*"
        },
        {
          Sid: "VisualEditor1",
          Action = "s3:ListAllMyBuckets",
          Effect = "Allow",
          Resource = "*"
        },
      ]
    })
  }

 inline_policy {
    name = "list_secrets_get_one_secret_value"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Sid: "VisualEditor0",
          Action = [
				"secretsmanager:GetSecretValue",
				"secretsmanager:DescribeSecret"
			],
          Effect = "Allow",
          Resource = "arn:aws:secretsmanager:us-east-1:210242717093:secret:prod/github-backup-u7Ivlh"
        },
        {
          Sid: "VisualEditor1",
          Action = "secretsmanager:ListSecrets",
          Effect = "Allow",
          Resource = "*"
        },
      ]
    })
  }
}
