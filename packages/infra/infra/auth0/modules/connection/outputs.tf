output "connection_id" {
  description = "The Auth0 connection id (con_...)."
  value       = auth0_connection.this.id
}

output "name" {
  description = "The connection name."
  value       = auth0_connection.this.name
}
