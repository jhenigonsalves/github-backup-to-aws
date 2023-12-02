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
          Sid : "VisualEditor0",
          Action = [
            "s3:PutObject",
            "s3:ListBucket",
            "s3:GetBucketPolicy"
          ],
          Effect   = "Allow",
          Resource = "arn:aws:s3:::${local.bucket_backup_name}/*"
        },
        {
          Sid : "VisualEditor1",
          Action   = "s3:ListAllMyBuckets",
          Effect   = "Allow",
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
          Sid : "VisualEditor0",
          Action = [
            "secretsmanager:GetSecretValue",
            "secretsmanager:DescribeSecret"
          ],
          Effect   = "Allow",
          Resource = local.backup_secret_arn
        },
        {
          Sid : "VisualEditor1",
          Action   = "secretsmanager:ListSecrets",
          Effect   = "Allow",
          Resource = "*"
        },
      ]
    })
  }
}


resource "aws_iam_role" "scheduler_invoke_lambda_role" {
  name = "scheduler_invoke_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "allow_invoke_lambda"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Sid : "VisualEditor0",
          Action = [
            "lambda:InvokeFunction"
          ],
          Effect   = "Allow",
          Resource = "*"
        },
      ]
    })
  }
}
