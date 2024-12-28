#Definition of RDS instance and related resources

resource "aws_db_instance" "mssql_db" {
  allocated_storage      = var.rdssql_db_storage
  engine                 = var.rdssql_db_engine
  engine_version         = var.rdssql_engine_version
  instance_class         = var.rdssql_db_instance_class
  license_model          = "license-included"
  port                   = 1433
  username               = var.rdssql_username
  password               = var.rdssql_password
  availability_zone      = var.deployment_az
  multi_az               = false
  db_subnet_group_name   = aws_db_subnet_group.mssql_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.db_sg_allow_ec2.id]
  option_group_name      = aws_db_option_group.db_option_group_sql_restore.name
  apply_immediately      = true
  skip_final_snapshot    = true

  tags = {
    Name = "AdventureWorks instance mssql server database"
  }
}


resource "aws_db_option_group" "db_option_group_sql_restore" {
  name                     = "db-option-group-sql-restore"
  option_group_description = "Allow sql restore"
  engine_name              = var.rdssql_db_engine
  major_engine_version     = var.rdssql_engine_version

  option {
    option_name = "SQLSERVER_BACKUP_RESTORE"
    option_settings {
      name  = "IAM_ROLE_ARN"
      value = aws_iam_role.backup_restore_role.arn
    }
  }
}

resource "aws_security_group" "db_sg_allow_ec2" {
  name        = "db_sg_allow_ec2"
  description = "Allow trafic coming from specific ecs cluster"
  vpc_id      = aws_vpc.mssql_db_vpc.id

  ingress {
    from_port       = 1433
    to_port         = 1433
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db_sg_allow_ec2"
  }
}

resource "aws_iam_role" "backup_restore_role" {
  name = "backup_restore_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "rds.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Description = "Policy attached to SQL Server Option Group to allow backup restore from S3 bucket"
  }
}


resource "aws_iam_role_policy" "backup_restore_role_policy" {
  name = "backup_restore_role_policy"
  role = aws_iam_role.backup_restore_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ],
        Resource = aws_s3_bucket.turing-aws-aw-backup.arn
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObjectAttributes",
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListMultipartUploadParts",
          "s3:AbortMultipartUpload"
        ],
        Resource = "${aws_s3_bucket.turing-aws-aw-backup.arn}/*"
      }
  ] })
}