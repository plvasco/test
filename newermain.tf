terraform {
required_providers {
aws = {
source = "hashicorp/aws"
version = "4.32.0"
}
}
}



provider "aws" {
region = "us-gov-east-1"
profile = "pietto"
}



provider "aws" {
region = var.region
profile = var.profile-remote
alias = "remote"
}



module "iam_read_only_user" {
source = "./build-modules/iam-read-only"
iam_policy_name = "e2g_ro_policy"
iam_role_name = "e2g_ro_role"
iam_role_trust_policy_list = ["codedeploy.amazonaws.com"]
}



module "vpc" {
source = "./build-modules/vpc-build"
providers = {
aws = aws
aws.remote = aws.remote
}
region = var.region
cs_account_id = var.cs_account_id
cs_transit_vpc = var.cs_transit_vpc
cs_transit_cidr = var.cs_transit_cidr
cs_transit_route_table = var.cs_transit_route_table
domain_name = "usdcag.aws.ray.com"
ntp_servers = ["10.250.0.12", "10.250.0.142"]
netbios_node_type = 2
}



output "vpc_id" {
value = module.vpc.vpc_id
}

your main.tf should have this

two provider config. aws and aws.remote.

as your vpc module has requirement for two aws providers

in vpc peering setup.

provider "aws" {
region = var.region
profile = var.profile-remote
alias = "remote"
}
