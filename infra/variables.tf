variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs to use for Aurora DB Subnet Group"
}

variable "aurora_db_version" {
  type        = string
  description = "Aurora DB Postgresql version"
}

variable "aurora_db_instance_class" {
  type        = string
  description = "Aurora DB instance type"
}

variable "environment" {
  type        = string
  description = "Environment"
  default     = "staging"
}

variable "vpc_id" {
  type        = string
  description = "VPC to use for Aurora DB"
}

variable "aws_region" {
  type = string
  description = "AWS REgion"
}

variable "k8s_black_cluster_sg_id" {
  type = string
  description = "Security group id of black EKS cluster"
}

variable "k8s_red_cluster_sg_id" {
  type = string
  description = "Security group id of red EKS cluster"
}

variable "k8s_red_vpc_cidr" {
  type = string
  description = "EKS Red cluster VPC CIDR"
}

variable "k8s_black_vpc_cidr" {
  type = string
  description = "EKS Black cluster VPC CIDR"
}

variable "util_vpc_cidr" {
  type        = string
  description = "Util VPC CIDR allowed to Aurora"
}

variable "eks_red_cluster_name" {
  type        = string
  description = "Name of the RED EKS cluster for IRSA setup"
}

variable "eks_black_cluster_name" {
  type        = string
  description = "Name of the BLACK EKS cluster for IRSA setup"
}

variable "kubernetes_namespace" {
  type        = string
  description = "Kubernetes namespace where the service account will be created"
  default     = "wms"
}

variable "service_account_name" {
  type        = string
  description = "Name of the Kubernetes service account"
  default     = "recipes-api-service"
}