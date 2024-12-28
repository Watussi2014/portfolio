# Definition of ECR repositories
resource "aws_ecr_repository" "db_restore" {
  name         = "database-restore"
  force_delete = true
}

resource "aws_ecr_repository" "db_analytics" {
  name         = "database-analytics"
  force_delete = true
}

#Creating the cluster
resource "aws_ecs_cluster" "main" {
  name = "main-ecs-cluster"
}

# Task definition for DB restore and db analytics. Calling image from created ECR
resource "aws_ecs_task_definition" "db_restore" {
  family                   = "db-restore"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "db-restore"
      image     = "${aws_ecr_repository.db_restore.repository_url}:latest"
      memory    = 512
      essential = true
      environment = [
        {
          name  = "DB_HOST"
          value = aws_db_instance.mssql_db.address
        },
        {
          name  = "DB_USER"
          value = aws_db_instance.mssql_db.username
        },
        {
          name  = "DB_PWD"
          value = aws_db_instance.mssql_db.password
        },
        {
          name  = "BACKUP_FILE_ARN"
          value = aws_s3_object.aw_db_backup.arn
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/db-restore"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
          "awslogs-create-group"  = "true"
        }
      }
    }
  ])
  depends_on = [aws_iam_role_policy_attachment.ecs_task_execution_role_policy]
}

resource "aws_ecs_task_definition" "db_analytics" {
  family                   = "db-analytics"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "db-analytics"
      image     = "${aws_ecr_repository.db_analytics.repository_url}:latest"
      memory    = 512
      essential = true
      environment = [
        {
          name  = "DB_HOST"
          value = aws_db_instance.mssql_db.address
        },
        {
          name  = "DB_USER"
          value = aws_db_instance.mssql_db.username
        },
        {
          name  = "DB_PWD"
          value = aws_db_instance.mssql_db.password
        },
        {
          name  = "S3_BUCKET"
          value = aws_s3_bucket.turing-aws-analysis-reports.id
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/db-analytics"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
          "awslogs-create-group"  = "true"
        }
      }
    }
  ])
  depends_on = [aws_iam_role_policy_attachment.ecs_task_execution_role_policy]
}

#State machine that runs the restore and analytics tasks inside the ecs cluster
resource "aws_sfn_state_machine" "db_workflow" {
  name     = "db-workflow"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    StartAt = "RestoreDatabase"
    States = {
      RestoreDatabase = {
        Type     = "Task"
        Resource = "arn:aws:states:::ecs:runTask.sync"
        Parameters = {
          LaunchType     = "FARGATE"
          Cluster        = aws_ecs_cluster.main.arn
          TaskDefinition = aws_ecs_task_definition.db_restore.arn
          NetworkConfiguration = {
            AwsvpcConfiguration = {
              Subnets        = [aws_subnet.mssql_db_subnet[0].id]
              SecurityGroups = [aws_security_group.ecs_tasks.id]
              AssignPublicIp = "DISABLED"
            }
          }
        }
        Next = "RunAnalytics"
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "FailState"
        }]
      }
      RunAnalytics = {
        Type     = "Task"
        Resource = "arn:aws:states:::ecs:runTask.sync"
        Parameters = {
          LaunchType     = "FARGATE"
          Cluster        = aws_ecs_cluster.main.arn
          TaskDefinition = aws_ecs_task_definition.db_analytics.arn
          NetworkConfiguration = {
            AwsvpcConfiguration = {
              Subnets        = [aws_subnet.mssql_db_subnet[0].id]
              SecurityGroups = [aws_security_group.ecs_tasks.id]
              AssignPublicIp = "DISABLED"
            }
          }
        }
        End = true
      }
      FailState = {
        Type  = "Fail"
        Cause = "Task Failed"
      }
    }
  })
}

#Ressources related to ECS and state machine
resource "aws_security_group" "ecs_tasks" {
  name        = "db-restore-ecs-tasks"
  description = "Allow traffic for ECS tasks"
  vpc_id      = aws_vpc.mssql_db_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Create IAM role for ECS task
resource "aws_iam_role" "ecs_task_role" {
  name = "ecs_task_role_analytics"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Create IAM policy for S3 access
resource "aws_iam_role_policy" "ecs_task_s3_policy" {
  name = "ecs_task_s3_policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.turing-aws-analysis-reports.arn}",
          "${aws_s3_bucket.turing-aws-analysis-reports.arn}/*"
        ]
      }
    ]
  })
}

#Policy to allow access to CloudWatch logs
resource "aws_iam_role_policy" "ecs_task_execution_cloudwatch" {
  name = "ecs-task-execution-cloudwatch"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/*",
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/*:log-stream:*"
        ]
      }
    ]
  })
}

# Step Function role
resource "aws_iam_role" "step_function_role" {
  name = "step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# Policy to allow Step Function to run ECS tasks
resource "aws_iam_role_policy" "step_function_policy" {
  name = "step-function-policy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecs:RunTask",
          "ecs:StopTask",
          "ecs:DescribeTasks",
          "iam:PassRole",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "events:PutTargets",
          "events:PutRule",
          "events:DescribeRule",
          "states:*"
        ]
        Resource = [
          "${aws_ecs_cluster.main.arn}",
          "${aws_ecs_task_definition.db_restore.arn}",
          "${aws_ecs_task_definition.db_analytics.arn}",
          "${aws_iam_role.ecs_task_execution_role.arn}",
          "arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:task/*",
          "arn:aws:events:${var.aws_region}:${data.aws_caller_identity.current.account_id}:rule/*",
          "arn:aws:states:${var.aws_region}:${data.aws_caller_identity.current.account_id}:stateMachine:*"
        ]
      },
      {
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = [
          "${aws_iam_role.ecs_task_execution_role.arn}",
          "${aws_iam_role.ecs_task_role.arn}"
        ]
      }
    ]
  })
}
