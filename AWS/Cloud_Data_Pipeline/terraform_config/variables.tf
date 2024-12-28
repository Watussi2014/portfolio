# General variables

variable "aws_region" {
  type        = string
  default     = "eu-west-3"
  description = "AWS Region"
}

variable "deployment_az" {
  type        = string
  default     = "eu-west-3a"
  description = "AWS deployment Availability Zone"
}



# RDS Instance variables

variable "rdssql_db_engine" {
  type        = string
  default     = "sqlserver-ex"
  description = "SQL Server Express Edition Version"
}

variable "rdssql_engine_version" {
  type        = string
  default     = "16.00"
  description = "MSSQL Engine Version"
}

variable "rdssql_db_storage" {
  type        = number
  default     = 20
  description = "Database storage in GB"
}

variable "rdssql_password" {
  type        = string
  default     = "MyStrongPa$$w0rd"
  description = "RDS Admin password"
  sensitive   = true
}

variable "rdssql_db_instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "Amazon RDS DB Instance class"
}

variable "rdssql_db_name" {
  type        = string
  default     = "AdventureWorks"
  description = "RDS DB Name"
}

variable "rdssql_username" {
  type        = string
  default     = "admin"
  description = "RDS DB Username"
}