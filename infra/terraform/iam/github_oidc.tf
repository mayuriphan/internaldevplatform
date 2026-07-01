###############################################
# GitHub Actions OIDC Provider
###############################################

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]
}

###############################################
# GitHub OIDC Trust Policy
###############################################

data "aws_iam_policy_document" "github_oidc_assume_role" {

  statement {

    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type = "Federated"

      identifiers = [
        aws_iam_openid_connect_provider.github.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        "repo:${var.github_owner}/${var.github_repo}:ref:refs/heads/main"
      ]
    }
  }
}

###############################################
# IAM Role
###############################################

resource "aws_iam_role" "github_actions" {

  name = "github-actions-idp"

  assume_role_policy = data.aws_iam_policy_document.github_oidc_assume_role.json
}

###############################################
# Attach ECR Permissions
###############################################

resource "aws_iam_role_policy_attachment" "ecr" {

  role = aws_iam_role.github_actions.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}