module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "idp-eks"
  cluster_version  = "1.36"

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_endpoint_public_access_cidrs = ["182.70.209.90/32"]

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  enable_irsa = true

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      max_size     = 5
      min_size     = 1

      instance_types = ["t3.medium"]
    }
  }

  tags = {
    Project = "idp-platform"
  }
}