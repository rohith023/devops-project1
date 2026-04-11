variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "drug-app"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet CIDR"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDRs"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
}

variable "instance_type" {
  description = "EC2/EKS instance type"
  type        = string
  default     = "t3.medium"
}

variable "min_nodes" {
  description = "Minimum EKS nodes"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum EKS nodes"
  type        = number
  default     = 5
}

variable "desired_nodes" {
  description = "Desired EKS nodes"
  type        = number
  default     = 2
}
