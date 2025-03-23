variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "ecr_repository_name" {
  description = "Name for the ECR repository"
  type        = string
  default     = "nba-data-repo"
}

variable "data_bucket_name" {
  description = "Name of the S3 bucket to store NBA data"
  type        = string
  default     = "nba-data-stats"
}

variable "vpc_id" {
  description = "VPC ID for security group"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for ECS tasks"
  type        = string
}

variable "task_cpu" {
  description = "CPU units for ECS task"
  type        = string
  default     = "4096" # 4 vCPU
}

variable "task_memory" {
  description = "Memory for ECS task in MB"
  type        = string
  default     = "8192" # 8 GB
}
