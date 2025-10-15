data "aws_caller_identity" "current" {}


data "aws_eks_cluster" "red_cluster" {
  name = var.eks_red_cluster_name
}


data "aws_eks_cluster" "black_cluster" {
  name = var.eks_black_cluster_name
}

resource "aws_iam_role" "recipes_api_parameter_store_role" {
  name = "${var.environment}-recipes-api-parameter-store-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(data.aws_eks_cluster.red_cluster.identity[0].oidc[0].issuer, "https://", "")}"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${replace(data.aws_eks_cluster.red_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub" = "system:serviceaccount:${var.kubernetes_namespace}:${var.service_account_name}"
            "${replace(data.aws_eks_cluster.red_cluster.identity[0].oidc[0].issuer, "https://", "")}:aud" = "sts.amazonaws.com"
          }
        }
      },
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(data.aws_eks_cluster.black_cluster.identity[0].oidc[0].issuer, "https://", "")}"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${replace(data.aws_eks_cluster.black_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub" = "system:serviceaccount:${var.kubernetes_namespace}:${var.service_account_name}"
            "${replace(data.aws_eks_cluster.black_cluster.identity[0].oidc[0].issuer, "https://", "")}:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-recipes-api-parameter-store-role"
    Environment = var.environment
    Service     = "recipes-api-service"
  }
}

resource "aws_iam_policy" "recipes_api_parameter_store_policy" {
  name        = "${var.environment}-recipes-api-parameter-store-policy"
  description = "Policy for Recipes API Service to access Parameter Store"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:PutParameter"
        ]
        Resource = [
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.environment}/applications/wms/recipes-api-service/environment/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = [
          "arn:aws:kms:${var.aws_region}:${data.aws_caller_identity.current.account_id}:key/*"
        ]
        Condition = {
          StringEquals = {
            "kms:ViaService" = "ssm.${var.aws_region}.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-recipes-api-parameter-store-policy"
    Environment = var.environment
    Service     = "recipes-api-service"
  }
}

resource "aws_iam_role_policy_attachment" "recipes_api_parameter_store_attachment" {
  role       = aws_iam_role.recipes_api_parameter_store_role.name
  policy_arn = aws_iam_policy.recipes_api_parameter_store_policy.arn
}
