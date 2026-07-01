data "aws_iam_policy_document" "eks_sqs" {
  statement {
    actions = [
      "sqs:*"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "sqs_policy" {
  name   = "idp-sqs-policy"
  policy = data.aws_iam_policy_document.eks_sqs.json
}