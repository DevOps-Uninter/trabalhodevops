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

# Bloco de configuração do provedor AWS
provider "aws" {
  region = "sa-east-1"
}

# Variável para o seu endereço de IP (pode ser usada no SG)
variable "my_ip_cidr" {
  type        = string
  description = "O CIDR do seu IP para acesso SSH"
  default     = "0.0.0.0/0" # Por enquanto aberto para o GitHub Actions
}

# -----------------------
# Rede (VPC, Subnet, IGW)
# -----------------------
resource "aws_vpc" "easyorder_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "easyorder-vpc"
  }
}

resource "aws_internet_gateway" "easyorder_igw" {
  vpc_id = aws_vpc.easyorder_vpc.id
  tags = {
    Name = "easyorder-igw"
  }
}

resource "aws_subnet" "easyorder_subnet_public" {
  vpc_id                  = aws_vpc.easyorder_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "sa-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "easyorder-subnet-public"
  }
}

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

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.easyorder_subnet_public.id
  route_table_id = aws_route_table.easyorder_rt.id
}

# ------------------------
# Segurança (Security Group)
# ------------------------
resource "aws_security_group" "easyorder_sg" {
  name        = "easyorder-sg"
  description = "Permite acesso SSH e API"
  vpc_id      = aws_vpc.easyorder_vpc.id

  ingress {
    description = "SSH (usado pelo GitHub Actions)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API access"
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

# ------------------------
# Chave SSH
# ------------------------
resource "aws_key_pair" "easyorder_key" {
  key_name   = "easyorder-key"
  public_key = file("~/.ssh/easyorder_key.pub")
}

# ------------------------
# IAM Role para CloudWatch
# ------------------------
resource "aws_iam_role" "ec2_role" {
  name = "easyorder-ec2-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cloudwatch_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "easyorder-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# ------------------------
# EC2 Instance
# ------------------------
resource "aws_instance" "easyorder" {
  ami                         = "ami-043edbf44f50364c5" # Ubuntu 22.04 em sa-east-1
  instance_type               = "t3.micro"
  key_name                    = aws_key_pair.easyorder_key.key_name
  subnet_id                   = aws_subnet.easyorder_subnet_public.id
  vpc_security_group_ids      = [aws_security_group.easyorder_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  tags = {
    Name = "easyorder-instance"
  }
}

# ------------------------
# Output
# ------------------------
output "instance_public_ip" {
  description = "O IP público da instância EC2"
  value       = aws_instance.easyorder.public_ip
}
