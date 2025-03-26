terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "nba-data-terraform-state"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

# ECR repository.
resource "aws_ecr_repository" "nba_data_repo" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECR repository policy to remove untagged images after 30 days.
resource "aws_ecr_lifecycle_policy" "nba_data_lifecycle_policy" {
  repository = aws_ecr_repository.nba_data_repo.name

  policy = jsonencode(
    {
      rules = [
        {
          rulePriority = 1
          description  = "Remove untagged images after 30 days"
          selection = {
            tagStatus   = "untagged"
            countType   = "sinceImagePushed"
            countUnit   = "days"
            countNumber = 30
          }
          action = {
            type = "expire"
          }
        }
      ]
    }
  )
}

# CloudWatch log group.
resource "aws_cloudwatch_log_group" "nba_data_log_group" {
  name              = "/ecs/nba-data-task"
  retention_in_days = 30
}

# ECS cluster.
resource "aws_ecs_cluster" "nba_data_cluster" {
  name = "nba-data-cluster"

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
      log_configuration {
        cloud_watch_log_group_name = aws_cloudwatch_log_group.nba_data_log_group.name
      }
    }
  }
}

# ECS task execution role.
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "nba-data-ecs-task-execution-role"

  assume_role_policy = jsonencode(
    {
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
    }
  )
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS task role with S3 permissions for storing data.
resource "aws_iam_role" "ecs_task_role" {
  name = "nba-data-ecs-task-role"

  assume_role_policy = jsonencode(
    {
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
    }
  )
}

resource "aws_iam_policy" "s3_access_policy" {
  name        = "nba-data-s3-access-policy"
  description = "Allow ECS tasks to access S3 for storing NBA data"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "s3:PutObject",
            "s3:GetObject",
            "s3:ListObject",
            "s3:DeleteObject",
          ]
          Resource = [
            "arn:aws:s3:::${var.data_bucket_name}",
            "arn:aws:s3:::${var.data_bucket_name}/*"
          ]
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "s3_access_policy_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# S3 bucket for storing the processed data.
resource "aws_s3_bucket" "nba_data_bucket" {
  bucket = var.data_bucket_name
}

resource "aws_s3_bucket_versioning" "nba_data_bucket_versioning" {
  bucket = aws_s3_bucket.nba_data_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "nba_data_bucket_encryption" {
  bucket = aws_s3_bucket.nba_data_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ECS task definition.
resource "aws_ecs_task_definition" "nba_data_task" {
  family                   = "nba-data-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode(
    [
      {
        name      = "nba-data-container"
        image     = "${aws_ecr_repository.nba_data_repo.repository_url}:latest"
        essential = true
        environemt = [
          { name = "S3_BUCKET", value = var.data_bucket_name }
        ]

        logConfiguration = {
          logDriver = "awslogs"
          options = {
            "awslogs-group"         = aws_cloudwatch_log_group.nba_data_log_group.name
            "awslogs-region"        = var.aws_region
            "awslogs-stream-prefix" = "ecs"
          }
        }
    }]
  )
}

# Lambda function to trigger ECS task.
resource "aws_lambda_function" "nba_data_trigger" {
  function_name = "nba-data-trigger"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_func.trigger_ecs_task_handler"
  runtime       = "python3.12"
  timeout       = 60

  filename         = data.archive_file.lambda_code.output_path
  source_code_hash = data.archive_file.lambda_code.output_base64sha256

  environment {
    variables = {
      CLUSTER_NAME      = aws_ecs_cluster.nba_data_cluster.name
      TASK_DEFINITION   = aws_ecs_task_definition.nba_data_task.arn
      SUBNET_ID         = var.subnet_id
      SECURITY_GROUP_ID = aws_security_group.ecs_tasks.id
    }
  }
}

data "archive_file" "lambda_code" {
  type        = "zip"
  source_file = "${path.module}/lambda/lambda_func.py"
  output_path = "${path.module}/lambda/lambda_func.zip"
}

# IAM role for Lambda.
resource "aws_iam_role" "lambda_role" {
  name = "nba-data-lambda-role"

  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        }
      ]
    }
  )
}

# IAM policy for Lambda to invoke ECS tasks.
resource "aws_iam_policy" "lambda_ecs_policy" {
  name        = "nba-data-lambda-ecs-policy"
  description = "Allow Lambda to run ECS tasks"

  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["ecs:RunTask"]
          Effect   = "Allow"
          Resource = aws_ecs_task_definition.nba_data_task.arn
        },
        {
          Action = ["iam:PassRole"]
          Effect = "Allow"
          Resource = [
            aws_iam_role.ecs_task_execution_role.arn,
            aws_iam_role.ecs_task_role.arn
          ]
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "lambda_logs_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_ecs_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_ecs_policy.arn
}

# Security group for ECS tasks.
resource "aws_security_group" "ecs_tasks" {
  name        = "nba-data-ecs-tasks-sg"
  description = "Allow outbound traffic from ECS tasks"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EventBridge rule for scheduled execution (one per year)
resource "aws_cloudwatch_event_rule" "nba_data_annual_trigger" {
  name                = "nba-data-annual-trigger"
  description         = "Trigger NBA data collection & extraction annually on May 1st"
  schedule_expression = "cron(0 0 1 5 ? *)" # Run at midnight on May 1st
}

resource "aws_cloudwatch_event_target" "nba_data_lambda_target" {
  rule      = aws_cloudwatch_event_rule.nba_data_annual_trigger.name
  target_id = "InvokeLambda"
  arn       = aws_lambda_function.nba_data_trigger.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.nba_data_trigger.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.nba_data_annual_trigger.arn
}
