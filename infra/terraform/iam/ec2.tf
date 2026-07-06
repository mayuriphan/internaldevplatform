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