terraform {
  required_version = ">= 1.10, < 2.0"

  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.3"
    }
  }
}

# Provider credentials come from environment variables:
#   RENDER_API_KEY, RENDER_OWNER_ID
provider "render" {}

# Owner-level project + environment grouping. Applied FIRST: environments are
# minted here and their evm-... IDs are hand-copied into each
# environments/<env> root module (no cross-workspace data source).
resource "render_project" "this" {
  name = "__YURT_PROJECT_NAME__"

  environments = {
    "staging" = {
      name             = "Staging"
      protected_status = "unprotected"
      network_isolated = false
    }
    "production" = {
      name             = "Production"
      protected_status = "protected"
      network_isolated = true
    }
  }
}

output "environment_ids" {
  description = "Map of environment key to Render environment ID (evm-...)"
  value       = { for k, v in render_project.this.environments : k => v.id }
}
