resource "random_password" "aurora_master_password" {
  length  = 32
  special = false
  upper   = true
  numeric = true
  lower   = true

  lifecycle {
    ignore_changes = all
  }
}

resource "random_password" "postgresql_deploy_user" {
  length  = 32
  special = false
  upper   = true
  numeric = true
  lower   = true

  lifecycle {
    ignore_changes = all
  }
}

resource "random_password" "postgresql_service_user" {
  length  = 32
  special = false
  upper   = true
  numeric = true
  lower   = true

  lifecycle {
    ignore_changes = all
  }
}