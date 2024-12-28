#Definition of different network ressources

resource "aws_vpc" "mssql_db_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "mssql_db_vpc"
  }
}

resource "aws_subnet" "mssql_db_subnet" {
  count                   = 3
  vpc_id                  = aws_vpc.mssql_db_vpc.id
  cidr_block              = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"][count.index]
  availability_zone       = [var.deployment_az, "eu-west-3b", "eu-west-3c"][count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "adventureworks database subnets"
  }
}

resource "aws_db_subnet_group" "mssql_db_subnet_group" {
  name       = "mssql_db_subnet_group"
  subnet_ids = [aws_subnet.mssql_db_subnet[0].id, aws_subnet.mssql_db_subnet[1].id, aws_subnet.mssql_db_subnet[2].id]

  tags = {
    Name = "adventureworks database subnet group"
  }
}

# VPC Endpoints
resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id              = aws_vpc.mssql_db_vpc.id
  service_name        = "com.amazonaws.eu-west-3.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.mssql_db_subnet[*].id
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true

  tags = {
    Name = "ECR Docker VPC Endpoint"
  }
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.mssql_db_vpc.id
  service_name        = "com.amazonaws.eu-west-3.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.mssql_db_subnet[*].id
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true

  tags = {
    Name = "ECR API VPC Endpoint"
  }
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.mssql_db_vpc.id
  service_name      = "com.amazonaws.eu-west-3.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]

  tags = {
    Name = "S3 Gateway VPC Endpoint"
  }
}

resource "aws_vpc_endpoint" "logs" {
  vpc_id              = aws_vpc.mssql_db_vpc.id
  service_name        = "com.amazonaws.eu-west-3.logs"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.mssql_db_subnet[*].id
  security_group_ids  = [aws_security_group.vpc_endpoint.id]
  private_dns_enabled = true

  tags = {
    Name = "CloudWatch Logs VPC Endpoint"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.mssql_db_vpc.id

  tags = {
    Name = "Private Route Table"
  }
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.mssql_db_subnet)
  subnet_id      = aws_subnet.mssql_db_subnet[count.index].id
  route_table_id = aws_route_table.private.id
}

resource "aws_security_group" "vpc_endpoint" {
  name        = "vpc-endpoints"
  description = "Security group for VPC endpoints"
  vpc_id      = aws_vpc.mssql_db_vpc.id

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "VPC Endpoint Security Group"
  }
}