resource "aws_sqs_queue" "job_queue" {
  name = "idp-job-queue"

  visibility_timeout_seconds = 60

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "dlq" {
  name = "idp-job-dlq"
}