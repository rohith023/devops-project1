output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.drug_recommendation_vpc.id
}

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = aws_subnet.public.id
}

output "private_subnet_id" {
  description = "Private Subnet ID"
  value       = aws_subnet.private.id
}

output "security_group_id" {
  description = "Security Group ID"
  value       = aws_security_group.drug_recommendation_sg.id
}

output "ec2_instance_id" {
  description = "EC2 Instance ID"
  value       = try(aws_instance.drug_recommendation_instance[0].id, null)
}

output "ec2_instance_public_ip" {
  description = "EC2 Instance Public IP"
  value       = try(aws_eip.drug_recommendation_eip[0].public_ip, null)
}

output "ec2_instance_private_ip" {
  description = "EC2 Instance Private IP"
  value       = try(aws_instance.drug_recommendation_instance[0].private_ip, null)
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group Name"
  value       = aws_cloudwatch_log_group.drug_recommendation_logs.name
}

output "app_url" {
  description = "Application URL"
  value       = try("http://${aws_eip.drug_recommendation_eip[0].public_ip}:5000", null)
}
