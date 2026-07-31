output "job_queue_arn" {
  value = aws_sqs_queue.job_queue.arn
}

output "dlq_arn" {
  value = aws_sqs_queue.dlq.arn
}