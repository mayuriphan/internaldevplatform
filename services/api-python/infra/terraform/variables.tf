variable "db_password" {
  type    = string
  default = "MyDbPass123"
}

variable "aws_region" {
  default = "ap-south-1"
}

variable "instance_type" {
  default = "t3.small"
}

variable "key_name" {
  default = var.key_name
}

variable "ip" {
  default = var.ip
}

variable "ami" {
  default = var.ami
}