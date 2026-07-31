###############################################
# EC2 Role
###############################################

data "aws_iam_policy_document" "ec2_assume_role" {

  statement {

    effect = "Allow"

    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"

      identifiers = [
        "ec2.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "k3s" {

  name = "k3s-ec2-role"

  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

###############################################
# Allow pulling images from ECR
###############################################

resource "aws_iam_role_policy_attachment" "k3s_ecr" {

  role = aws_iam_role.k3s.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

###############################################
# Instance Profile
###############################################

resource "aws_iam_instance_profile" "k3s" {

  name = "k3s-instance-profile"

  role = aws_iam_role.k3s.name
}

###############################################
# Allow reading Secrets Manager
###############################################

resource "aws_iam_policy" "k3s_secrets_manager" {
  name = "k3s-secrets-manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = "arn:aws:secretsmanager:ap-south-1:187457215475:secret:idp/prod/app*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "k3s_secrets_manager" {
  role       = aws_iam_role.k3s.name
  policy_arn = aws_iam_policy.k3s_secrets_manager.arn
}

resource "aws_iam_policy" "k3s_sqs" {
  name = "k3s-sqs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl",
          "sqs:ChangeMessageVisibility"
        ]
        Resource = [
          var.job_queue_arn,
          var.dlq_arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "k3s_sqs" {
  role       = aws_iam_role.k3s.name
  policy_arn = aws_iam_policy.k3s_sqs.arn
}