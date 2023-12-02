resource "aws_s3_bucket" "github_backup" {
  bucket        = local.bucket_backup_name
  force_destroy = true
}


resource "aws_s3_bucket_lifecycle_configuration" "backup_lifecycle" {
  bucket = aws_s3_bucket.github_backup.id

  rule {
    id = "backup_lifecycle"

    expiration {
      days = 1825
    }

    status = "Enabled"


    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }

}
