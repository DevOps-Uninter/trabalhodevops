# Bloco de configuração do Terraform
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provedor AWS
provider "aws" {
  region = "sa-east-1"
}

# Variável para o IP local (se quiser restringir o SSH depois)
variable "my_ip_cidr" {
  type        = string
  description = "O CIDR do seu IP para acesso SSH"
  default     = "0.0.0.0/0" # permite de qualquer lugar, mas pode trocar pelo seu IP
}

# VPC
resource "aws_vpc" "easyorder_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "easyorder-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "easyorder_igw" {
  vpc_id = aws_vpc.easyorder_vpc.id
  tags = {
    Name = "easyorder-igw"
  }
}

# Subnet pública
resource "aws_subnet" "easyorder_subnet_public" {
  vpc_id                  = aws_vpc.easyorder_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "sa-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "easyorder-subnet-public"
  }
}

# Route table
resource "aws_route_table" "easyorder_rt" {
  vpc_id = aws_vpc.easyorder_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.easyorder_igw.id
  }
  tags = {
    Name = "easyorder-rt-public"
  }
}

# Associação da subnet à route table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.easyorder_subnet_public.id
  route_table_id = aws_route_table.easyorder_rt.id
}

# Security group (firewall)
resource "aws_security_group" "easyorder_sg" {
  name        = "easyorder-sg"
  description = "Permite acesso SSH e API para a instancia EasyOrder"
  vpc_id      = aws_vpc.easyorder_vpc.id

  ingress {
    description = "SSH (para CI/CD e desenvolvedores)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  ingress {
    description = "API access (porta 8000)"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "easyorder-sg"
  }
}

# Key pair
resource "aws_key_pair" "easyorder_key" {
  key_name   = "easyorder-key"
  public_key = file("~/.ssh/easyorder_key.pub")
}


data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical (Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Instância EC2
resource "aws_instance" "easyorder" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = aws_key_pair.easyorder_key.key_name
  subnet_id     = aws_subnet.easyorder_subnet_public.id
  vpc_security_group_ids = [aws_security_group.easyorder_sg.id]

  tags = {
    Name = "easyorder-instance"
  }
}

# Output para mostrar IP público
output "instance_public_ip" {
  description = "O IP publico da instancia EC2"
  value       = aws_instance.easyorder.public_ip
}
