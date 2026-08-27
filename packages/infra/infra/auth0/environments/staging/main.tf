terraform {
  required_version = ">= 1.10, < 2.0"

  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.41"
    }
  }
}

# Provider credentials come from environment variables:
#   AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
provider "auth0" {}

# Adopt the IaC app's manually-bootstrapped Management API grant.
# One-shot: no-ops once the grant is in state.
#
# UNCOMMENT in Phase 3 step 6 (infra/README.md): fill in the cgr_... ID
# recorded during Phase 1, and flip manage_iac_grant below to true in the
# same apply. Left commented until then because an import block with a
# placeholder ID fails `terraform plan`.
#
# import {
#   to = module.auth0_tenant.module.iac_grant.auth0_client_grant.terraform_iac[0]
#   id = "cgr_REPLACE_ME"
# }

module "auth0_tenant" {
  source = "../../modules/tenant"

  tenant_name    = "Staging"
  api_identifier = "__YURT_API_IDENTIFIER__"

  # The staging frontend's URL. Replace after the Render static site exists
  # (Phase 3 step 4, infra/README.md) — usually
  # https://<project>-staging-frontend.onrender.com (Render only appends a
  # random suffix on a name collision).
  app_url = "https://REPLACE_ME.onrender.com"

  # Local dev against the staging tenant (Vite dev server).
  additional_app_urls = [
    "http://localhost:3000",
  ]

  # Flip to true in Phase 3 step 6 together with the import block above, once
  # the hand-made "Terraform IaC" grant has been recorded.
  manage_iac_grant = false

  # Tenant custom domain is off by default (and requires a credit card on file
  # with Auth0) — see "Auth0 custom domains" in infra/README.md to add one:
  #
  # custom_domain        = "staging.auth.example.com"
  # verify_custom_domain = false # flip to true after the CNAME exists in DNS
}

output "spa_client_id" {
  value = module.auth0_tenant.spa_client_id
}

output "api_identifier" {
  value = module.auth0_tenant.api_identifier
}

output "custom_domain_verification_records" {
  value = module.auth0_tenant.custom_domain_verification_records
}

output "custom_domain_status" {
  value = module.auth0_tenant.custom_domain_status
}
