output "spa_client_id" {
  description = "Client ID for the SPA application (frontend VITE_AUTH0_CLIENT_ID)"
  value       = auth0_client.spa.client_id
}

output "api_identifier" {
  description = "Auth0 API audience identifier (frontend VITE_AUTH0_AUDIENCE)"
  value       = auth0_resource_server.api.identifier
}

output "custom_domain_verification_records" {
  description = "DNS records the registrar needs before verify_custom_domain can pass (empty until custom_domain is set)"
  value       = var.custom_domain == null ? [] : auth0_custom_domain.tenant[0].verification[0].methods
}

output "custom_domain_status" {
  description = "Configuration status of the custom domain (ready = serving auth traffic)"
  value       = var.custom_domain == null ? null : auth0_custom_domain.tenant[0].status
}
