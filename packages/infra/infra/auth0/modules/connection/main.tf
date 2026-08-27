terraform {
  required_version = ">= 1.10, < 2.0"

  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.41"
    }
  }
}

# Baseline connection module for the uniform database / social connections.
# Terraform owns the connection's existence and, authoritatively, which apps it
# is enabled on. The connection's detailed options (password policy, MFA,
# passkeys, social scopes) are operational settings managed in the Auth0
# dashboard, not here, so they are left under ignore_changes.
resource "auth0_connection" "this" {
  name           = var.name
  strategy       = var.strategy
  display_name   = var.display_name
  show_as_button = var.show_as_button
  realms         = var.realms

  # Options are owned in the Auth0 dashboard; ignore_changes keeps Terraform from
  # touching them while still managing the connection's existence and enablement.
  options {}

  lifecycle {
    ignore_changes = [options]
  }
}

# Authoritative enablement: the complete set of apps this connection is on.
# An empty list disables the connection everywhere.
#
# This resource cannot be created against a connection that already has clients
# attached; adopting an existing connection requires importing it (id = the
# connection ID) alongside the connection itself.
resource "auth0_connection_clients" "this" {
  connection_id   = auth0_connection.this.id
  enabled_clients = var.enabled_client_ids
}
