resource "aws_db_subnet_group" "aurora_subnet_group" {
  name       = "recipes-api-db-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_rds_cluster" "aurora_cluster" {
  cluster_identifier     = "recipes-api-db"
  engine                 = "aurora-postgresql"
  engine_version         = var.aurora_db_version
  master_username         = "superuser"
  master_password        = data.aws_ssm_parameter.aurora_master_password.value
  db_subnet_group_name   = aws_db_subnet_group.aurora_subnet_group.name
  vpc_security_group_ids = [aws_security_group.aurora_sg.id]
  storage_encrypted      = true
  deletion_protection    = true
}

resource "aws_rds_cluster_instance" "aurora_writer" {
  identifier         = "recipes-api-db-writer"
  cluster_identifier = aws_rds_cluster.aurora_cluster.id
  instance_class     = var.aurora_db_instance_class
  engine             = aws_rds_cluster.aurora_cluster.engine
}

resource "aws_rds_cluster_instance" "aurora_read_replica" {
  identifier          = "recipes-api-db-read-replica"
  cluster_identifier  = aws_rds_cluster.aurora_cluster.id
  instance_class      = var.aurora_db_instance_class
  engine              = aws_rds_cluster.aurora_cluster.engine
  publicly_accessible = false
}