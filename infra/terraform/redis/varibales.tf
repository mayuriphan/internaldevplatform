variable "vpc_id" {
  type = string
}

variable "k3s_security_group_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}