output "github_actions_role_arn" {
  value = aws_iam_role.github_actions.arn
}

output "k3s_instance_profile_name" {
  value = aws_iam_instance_profile.k3s.name
}