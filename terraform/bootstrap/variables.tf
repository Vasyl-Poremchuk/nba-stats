variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "terraform_state_bucket" {
  description = "Name for the S3 bucket to store Terraform state"
  type        = string
  default     = "nba-data-terraform-state"
}

variable "terraform_state_lock_table" {
  description = "Name for the DynamoDB table for Terraform state locking"
  type        = string
  default     = "nba-data-terraform-state-lock"
}
