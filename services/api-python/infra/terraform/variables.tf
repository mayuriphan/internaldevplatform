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
  type    = string
}

variable "ip" {
  type    = string
}

variable "ami" {
  type    = string
}