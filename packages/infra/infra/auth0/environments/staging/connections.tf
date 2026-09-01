# Adopts the staging tenant's default connections and sets their app enablement
# to the intended state:
#   - Username-Password-Authentication -> Staging SPA only (the login path)
#   - google-oauth2                    -> none (disabled everywhere)
#
# A fresh Auth0 tenant auto-creates both connections, so they must be ADOPTED
# (imported), not created. Everything below ships commented out because import
# blocks with placeholder IDs fail `terraform plan`.
#
# UNCOMMENT in Phase 3 step 7 (infra/README.md): fill in the two con_... IDs
# recorded during Phase 1, uncomment every block below this header comment
# (the header itself stays commented), and apply. Until that
# apply runs, Auth0's tenant defaults are in effect — including google-oauth2
# enabled with Auth0's shared dev keys, so a Google button may appear on the
# login page. The apply below turns that off authoritatively (an empty
# enabled_client_ids list disables the connection on every app, and Terraform
# reverts dashboard re-enables on the next apply).
#
# Each connection takes two import blocks — one for the connection, one for its
# auth0_connection_clients enablement — both keyed by the same connection ID.
# The import blocks are one-shot: they no-op once the resources are in state.

# import {
#   to = module.connection_username_password.auth0_connection.this
#   id = "con_REPLACE_ME" # Username-Password-Authentication
# }

# import {
#   to = module.connection_username_password.auth0_connection_clients.this
#   id = "con_REPLACE_ME" # Username-Password-Authentication (same ID as above)
# }

# module "connection_username_password" {
#   source = "../../modules/connection"
#
#   name     = "Username-Password-Authentication"
#   strategy = "auth0"
#   realms   = ["Username-Password-Authentication"]
#
#   enabled_client_ids = [module.auth0_tenant.spa_client_id]
# }

# import {
#   to = module.connection_google_oauth2.auth0_connection.this
#   id = "con_REPLACE_ME" # google-oauth2
# }

# import {
#   to = module.connection_google_oauth2.auth0_connection_clients.this
#   id = "con_REPLACE_ME" # google-oauth2 (same ID as above)
# }

# module "connection_google_oauth2" {
#   source = "../../modules/connection"
#
#   name     = "google-oauth2"
#   strategy = "google-oauth2"
#   realms   = ["google-oauth2"]
#
#   enabled_client_ids = [] # adopted but disabled everywhere
# }
