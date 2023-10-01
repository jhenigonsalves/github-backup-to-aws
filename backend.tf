terraform {
  backend "s3" {
    region               = "us-east-1"
    bucket               = "jheni-tfstate"
    key                  = "github-backup/state.tfstate"
  }
}