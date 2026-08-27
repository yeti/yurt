output "frontend_id" {
  description = "Render static site ID"
  value       = render_static_site.frontend.id
}

output "frontend_url" {
  description = "Render static site URL"
  value       = render_static_site.frontend.url
}

output "backend_id" {
  description = "Render web service ID"
  value       = render_web_service.backend.id
}

output "backend_url" {
  description = "Render web service URL"
  value       = render_web_service.backend.url
}

output "database_id" {
  description = "Render PostgreSQL instance ID"
  value       = render_postgres.database.id
}

output "backend_env_group_id" {
  description = "Render env group ID linked to the backend service"
  value       = render_env_group.backend.id
}
