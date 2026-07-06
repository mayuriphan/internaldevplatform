module "vpc" {
  source = "./vpc"
}

module "rds" {
  source = "./rds"

  vpc_id     = module.vpc.vpc_id
  # subnet_ids = module.vpc.private_subnets
  subnet_ids = module.vpc.public_subnets
  db_password = var.db_password
  ip = var.ip
}

module "redis" {
  source = "./redis"

  subnet_ids = module.vpc.private_subnets
}

module "sqs" {
  source = "./sqs"
}

module "ecr" {
  source = "./ecr"
}

resource "aws_security_group" "k3s" {
  name = "k3s-sg"

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [var.ip]
  }

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "k3s" {
  ami           = var.ami
  instance_type = "t3.small"
  iam_instance_profile = module.iam.k3s_instance_profile_name
  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.k3s.id
  ]

  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "k3s-server"
  }
}

module "iam" {
  source = "./iam"
  github_owner = var.github_owner
  github_repo  = var.github_repo
}

# module "eks" {
#   source = "./eks"

#   vpc_id     = module.vpc.vpc_id
#   subnet_ids = module.vpc.private_subnets
# }
