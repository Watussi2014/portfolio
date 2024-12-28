resource "aws_s3_bucket" "turing-aws-aw-backup" {
  bucket = "turing-aws-aw-backup"
}

resource "aws_s3_object" "aw_db_backup" {
  bucket = aws_s3_bucket.turing-aws-aw-backup.bucket
  key    = "AW2022.bak"
  source = "../tmp/AdventureWorks2022.bak"
}

resource "aws_s3_bucket" "turing-aws-analysis-reports" {
  bucket        = "turing-aws-analysis-reports"
  force_destroy = true
}