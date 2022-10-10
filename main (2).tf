locals {
  subnets_info = {
    "common-a" = {
        availability_zone = "${var.region}a"
        cidr_block = cidrsubnet(local.tce_cidr, 2, 0)
        tags = {
          "Name" = "${local.tenant_name}-Common-A"
        }
        vpc_id = aws_vpc.common.id
      },
    "common-b" = {
        availability_zone = "${var.region}b"
        cidr_block = cidrsubnet(local.tce_cidr, 2, 1)
        tags = {
          "Name" = "${local.tenant_name}-Common-B"
        }
        vpc_id = aws_vpc.common.id
      },    
    "svc-a" = {
        availability_zone = "${var.region}a"
        cidr_block = local.svc_a
        tags = {
          "Name" = "${local.tenant_name}-SVC-A"
        }
        vpc_id = aws_vpc.common.id
      },    
    "svc-b" = {
        availability_zone = "${var.region}b"
        cidr_block = local.svc_b
        tags = {
          "Name" = "${local.tenant_name}-SVC-B"
        }
        vpc_id = aws_vpc.common.id
      },
    "private-lan-a" = {
        availability_zone = "${var.region}a"
        cidr_block = local.tme_a
        tags = {
          "Name" = "${local.tenant_name}-Private-LAN-A"
        }
        vpc_id = aws_vpc.common.id
      },    
    "private-lan-b" = {
        availability_zone = "${var.region}b"
        cidr_block = local.tme_b
        tags = {
          "Name" = "${local.tenant_name}-Private-LAN-B"
        }
        vpc_id = aws_vpc.common.id
        }
    }
}

resource "aws_vpc" "common" {
    cidr_block = local.tce_cidr
    instance_tenancy = "default"
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
        Name = "${local.tenant_name} Common Net"
    }
}

# associate a second cidr to the vpc
resource "aws_vpc_ipv4_cidr_block_association" "common" {
    vpc_id     = aws_vpc.common.id
    cidr_block = local.tme_cidr
}

resource "aws_subnet" "subnet" {
    for_each = local.subnets_info
    vpc_id = each.value.vpc_id
    cidr_block = each.value.cidr_block
    availability_zone = each.value.availability_zone
    tags = each.value.tags
}

output "aws_subnet_id" {
    value = aws_subnet.subnet["private-lan-a"].id
}