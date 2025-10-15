resource "aws_security_group" "aurora_sg" {
  vpc_id = data.aws_vpc.vpc.id

  ingress = [{
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = []
    description     = "PostgreSQL access"
    cidr_blocks     = [
      var.k8s_black_vpc_cidr,
      var.k8s_red_vpc_cidr,
      var.util_vpc_cidr,
    ]
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    self             = false
  }]
}