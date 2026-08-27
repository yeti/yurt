resource "auth0_resource_server" "api" {
  identifier = var.api_identifier
  name       = "__YURT_PROJECT_NAME__ API - ${var.tenant_name}"

  skip_consent_for_verifiable_first_party_clients = true
  allow_offline_access                            = true
  token_lifetime                                  = 3600 # 1 hour
  token_lifetime_for_web                          = 3600 # 1 hour
}
