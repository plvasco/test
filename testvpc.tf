module "vpc" {
source = "./modules/vpc"
providers = {
aws = aws
aws.remote = aws.remote
}
region = var.region
tenant_name = local.tenant_name
tme_cidr = local.tme_cidr
tce_cidr = local.tce_cidr
tme_a = local.tme_a
tme_b = local.tme_a
svc_a = local.svc_a
svc_b = local.svc_b
cs_account_id = var.cs_account_id
cs_transit_vpc = var.cs_transit_vpc
cs_transit_cidr = var.cs_transit_cidr
cs_transit_route_table = var.cs_transit_route_table
domain_name = "usdcag.aws.ray.com"
ntp_servers = ["10.250.0.12", "10.250.0.142"]
netbios_node_type = 2
}
