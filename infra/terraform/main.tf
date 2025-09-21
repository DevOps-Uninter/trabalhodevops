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

# Variável para o seu endereço de IP
variable "my_ip_cidr" {
  type        = string
  description = "O CIDR do seu IP para acesso SSH"
}

# A sua rede privada na nuvem (VPC)
resource "aws_vpc" "easyorder_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true # Necessário para a instância ter um nome DNS
  tags = {
    Name = "easyorder-vpc"
  }
}

# O "portão" para a internet
resource "aws_internet_gateway" "easyorder_igw" {
  vpc_id = aws_vpc.easyorder_vpc.id
  tags = {
    Name = "easyorder-igw"
  }
}

# A "rua" dentro da sua rede
resource "aws_subnet" "easyorder_subnet_public" {
  vpc_id                  = aws_vpc.easyorder_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "sa-east-1a"
  map_public_ip_on_launch = true # Atribui IP público automaticamente
  tags = {
    Name = "easyorder-subnet-public"
  }
}

# O "mapa" que liga a rua ao portão da internet
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

# Associação do mapa à rua
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.easyorder_subnet_public.id
  route_table_id = aws_route_table.easyorder_rt.id
}

# A "firewall" da sua instância
resource "aws_security_group" "easyorder_sg" {
  name        = "easyorder-sg"
  description = "Permite acesso SSH e API para a instancia EasyOrder"
  vpc_id      = aws_vpc.easyorder_vpc.id
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
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

# Recurso que carrega a sua chave pública para a AWS
resource "aws_key_pair" "easyorder_key" {
  key_name   = "easyorder-key"
  public_key = file("~/.ssh/easyorder_key.pub")
}

# O seu servidor na nuvem (Instância EC2)
resource "aws_instance" "easyorder" {
  ami           = "ami-043edbf44f50364c5"
  instance_type = "t3.micro"
  key_name      = aws_key_pair.easyorder_key.key_name
  # Coloca a instância na "rua" e na "firewall" corretas
  subnet_id              = aws_subnet.easyorder_subnet_public.id
  vpc_security_group_ids = [aws_security_group.easyorder_sg.id]
  tags = {
    Name = "easyorder-instance"
  }
}

# Bloco de output para mostrar o IP público da instância
output "instance_public_ip" {
  description = "O IP publico da instancia EC2"
  value       = aws_instance.easyorder.public_ip
}