output "aurora_cluster_endpoint" {
  value       = aws_rds_cluster.aurora_cluster.endpoint
  description = "The writer endpoint of the RDS cluster"
}

output "aurora_cluster_port" {
  value       = aws_rds_cluster.aurora_cluster.port
  description = "The port of the RDS cluster"
}

output "aurora_cluster_db_name" { 
  value = aws_ssm_parameter.db_name.value
  description = "Database Name"
  sensitive = true
}

output "aurora_db_deploy_username" { 
  value = data.aws_ssm_parameter.deploy_user_name.value
  description = "Database Deploy Username"
  sensitive = true
}

output "parameter_store_role_arn" {
  value       = aws_iam_role.recipes_api_parameter_store_role.arn
  description = "ARN of the IAM role for Parameter Store access"
}

output "parameter_store_role_name" {
  value       = aws_iam_role.recipes_api_parameter_store_role.name
  description = "Name of the IAM role for Parameter Store access"
}