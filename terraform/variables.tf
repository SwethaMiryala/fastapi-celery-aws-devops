variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "project_name" {
  type    = string
  default = "devops-assignment"
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Docker image tag for backend and worker (set to the git SHA by CI)."
}

variable "redis_node_type" {
  type    = string
  default = "cache.t3.micro"
}
