locals {
  base_urls         = concat([var.app_url], var.additional_app_urls)
  all_callback_urls = local.base_urls
  all_logout_urls   = local.base_urls
  all_web_origins   = local.base_urls
}

resource "auth0_client" "spa" {
  name        = "__YURT_PROJECT_NAME__ Frontend - ${var.tenant_name}"
  description = "SPA client for the __YURT_PROJECT_NAME__ frontend (${var.tenant_name})"
  app_type    = "spa"

  callbacks           = local.all_callback_urls
  allowed_logout_urls = local.all_logout_urls
  web_origins         = local.all_web_origins
  allowed_origins     = local.all_web_origins

  grant_types = [
    "authorization_code",
    "refresh_token",
  ]

  oidc_conformant = true

  refresh_token {
    rotation_type       = "rotating"
    expiration_type     = "expiring"
    token_lifetime      = 2592000 # 30 days
    idle_token_lifetime = 28800   # 8 hours
    leeway              = 10      # grace window (s) for RT reuse detection
  }

  jwt_configuration {
    alg                 = "RS256"
    lifetime_in_seconds = 36000 # 10 hours
  }
}

# PKCE: public SPA client authenticates with no client secret.
resource "auth0_client_credentials" "spa" {
  client_id             = auth0_client.spa.client_id
  authentication_method = "none"
}
