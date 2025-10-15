data "aws_ssm_parameter" "aurora_master_password" {
  name            = aws_ssm_parameter.aurora_master_password.name
  with_decryption = true
}

resource "aws_ssm_parameter" "aurora_master_password" {
  name        = "/${var.environment}/applications/recipes-api-service/environment/MASTER_DATABASE_PASSWORD"
  description = "Master password for DB"
  type        = "SecureString"
  value       = random_password.aurora_master_password.result
}

resource "aws_ssm_parameter" "postgresql_deploy_user_password" {
  name = "/${var.environment}/applications/recipes-api-service/environment/DEPLOY_DATABASE_PASSWORD"
  description = "Postgresql Deploy User Password"
  type        = "SecureString"
  value       = random_password.postgresql_deploy_user.result
}

resource "aws_ssm_parameter" "postgresql_service_user_password" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/SERVICE_DATABASE_PASSWORD"
  description = "Postgresql Service User Password"
  type        = "SecureString"
  value       = random_password.postgresql_service_user.result
}

resource "aws_ssm_parameter" "db_url" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/DATABASE_URL"
  description = "Recipes APIDatabase URL"
  type        = "String"
  value       = aws_rds_cluster.aurora_cluster.endpoint
}

resource "aws_ssm_parameter" "db_name" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/DATABASE_NAME"
  description = "Postgresql recipes_api_service_primary db name"
  type        = "String"
  value       = "recipes_api_service_primary"
}

resource "aws_ssm_parameter" "deploy_user_name" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/DEPLOY_USER_NAME"
  description = "Postgresql Deploy User name"
  type        = "String"
  value       = "recipes_api_deploy_primary"
}

data "aws_ssm_parameter" "deploy_user_name" {
  name            = aws_ssm_parameter.deploy_user_name.name
  with_decryption = true
}


resource "aws_ssm_parameter" "connect_client_id" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/CONNECT_CLIENT_ID"
  description = "Connect Client ID for CulOps API authentication"
  type        = "SecureString"
  value       = "PLACEHOLDER_UPDATE_WITH_REAL_VALUE" 

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "connect_client_secret" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/CONNECT_CLIENT_SECRET"
  description = "Connect Client Secret for CulOps API authentication"
  type        = "SecureString"
  value       = "PLACEHOLDER_UPDATE_WITH_REAL_VALUE" 

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "culops_access_token" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/CUL_OPS_ACCESS_TOKEN"
  description = "CulOps Access Token - managed by token refresh cron job"
  type        = "SecureString"
  value       = "PLACEHOLDER_VALUE" 

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "culops_refresh_token" {
  name        = "/${var.environment}/applications/wms/recipes-api-service/environment/CUL_OPS_REFRESH_TOKEN"
  description = "CulOps Refresh Token - managed by token refresh cron job"
  type        = "SecureString"
  value       = "PLACEHOLDER_VALUE" 

  lifecycle {
    ignore_changes = [value]
  }
}