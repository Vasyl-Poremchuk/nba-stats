output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.nba_data_repo.repository_url
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.nba_data_cluster.name
}

output "ecs_task_definition_arn" {
  description = "The ARN of the ECS task definition"
  value       = aws_ecs_task_definition.nba_data_task.arn
}

output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.nba_data_trigger.function_name
}

output "s3_bucket_name" {
  description = "The name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.nba_data_log_group.name
}
