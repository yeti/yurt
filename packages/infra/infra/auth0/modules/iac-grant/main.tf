# Terraform IaC bootstrap app — Management API grant.
#
# The "Terraform IaC" M2M app is the credential Terraform authenticates with, so
# Terraform cannot create it (chicken-and-egg): the app and its first grant are
# made by hand when the tenant is bootstrapped. Once it exists we import
# the grant (committed import block in the environment root) and manage the
# scope list from here.
#
# Gated on `manage_iac_grant` for per-tenant rollout: a tenant only starts
# managing this grant once its existing grant has been imported. Leaving the
# flag false avoids Auth0 rejecting a second grant for the same client +
# audience on apply.
#
# DO NOT drop the *:client_grants scopes from this list. Terraform authenticates
# as this app; removing them locks the *next* run out of managing any grant. (A
# single apply is safe — the run's token is already minted — but the run after
# would fail to authenticate for grant management.)

terraform {
  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.41"
    }
  }
}

variable "manage_iac_grant" {
  description = "Manage the Terraform IaC app's Management API grant in Terraform. Enable only after importing this tenant's existing grant (see infra/README.md)."
  type        = bool
  default     = false
}

variable "iac_app_name" {
  description = "Display name of the bootstrap Terraform M2M application to attach the grant to."
  type        = string
  default     = "Terraform IaC"

  validation {
    condition     = length(trimspace(var.iac_app_name)) > 0
    error_message = "iac_app_name must be a non-empty application name (the data.auth0_client lookup matches by name)."
  }
}

locals {
  # Single source of truth for the IaC app's Management API scopes — only what
  # this project's tenant module manages (clients, resource servers,
  # connections, and the grants themselves). *:client_grants are
  # self-management scopes; read the warning above before editing.
  iac_management_scopes = [
    "read:clients", "create:clients", "update:clients", "delete:clients",
    "read:resource_servers", "create:resource_servers", "update:resource_servers", "delete:resource_servers",
    "read:connections", "create:connections", "update:connections", "delete:connections",
    # Auth0 split connection `options` behind dedicated scopes: without
    # read:connections_options the Get/List Connection responses omit the
    # options block entirely, so the provider reads options as null.
    "read:connections_options", "update:connections_options",
    "read:client_grants", "create:client_grants", "update:client_grants", "delete:client_grants",
    "read:tenant_settings",
    # Required for the post-login Action (tenant module action.tf) and its trigger binding.
    "read:actions", "create:actions", "update:actions", "delete:actions",
    "read:triggers", "update:triggers",
    # Required for the tenant custom domain (tenant module custom_domain.tf);
    # create:custom_domains also covers the verify call.
    "read:custom_domains", "create:custom_domains", "update:custom_domains", "delete:custom_domains",
  ]
}

data "auth0_tenant" "current" {}

data "auth0_client" "terraform_iac" {
  count = var.manage_iac_grant ? 1 : 0
  name  = var.iac_app_name
}

resource "auth0_client_grant" "terraform_iac" {
  count = var.manage_iac_grant ? 1 : 0

  client_id = data.auth0_client.terraform_iac[0].client_id
  audience  = "https://${data.auth0_tenant.current.domain}/api/v2/"
  scopes    = local.iac_management_scopes
}
