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

module "environment" {
  source = "../../modules/environment"

  environment_name = "__YURT_PROJECT_NAME__ Production"
  # Minted by infra/render/project — apply that root module first, then replace
  # this placeholder with the production ID from its environment_ids output
  # (Phase 3 step 1, infra/README.md).
  environment_id = "evm-REPLACE_ME"
  region         = "oregon"
  branch         = "main"
  repo_url       = "__YURT_REPO_URL__"

  database_name = "__YURT_PROJECT_SLUG_UNDERSCORE___production_db"
  database_user = "__YURT_PROJECT_SLUG_UNDERSCORE___production_db_user"

  # Custom domains are off by default; services use their *.onrender.com URLs.
  # To add them later, see "Custom domains" in infra/README.md:
  #
  # frontend_custom_domains = [
  #   { name = "app.example.com" },
  # ]
  #
  # backend_custom_domains = [
  #   { name = "api.example.com" },
  # ]
}

output "frontend_url" {
  value = module.environment.frontend_url
}

output "backend_url" {
  value = module.environment.backend_url
}
