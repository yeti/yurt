# Post-login Action stamping profile claims onto access tokens for the
# backend's JIT provisioning (see post-login-action.js).

resource "auth0_action" "stamp_profile_claims" {
  name    = "Stamp Profile Claims"
  runtime = "node22"
  deploy  = true

  supported_triggers {
    id      = "post-login"
    version = "v3"
  }

  code = file("${path.module}/post-login-action.js")

  lifecycle {
    # The JS hardcodes the claim namespace; fail the plan if it ever drifts
    # from the tenant's api_identifier (the backend reads `<audience>/email`).
    precondition {
      condition     = strcontains(file("${path.module}/post-login-action.js"), "const ns = \"${var.api_identifier}\";")
      error_message = "post-login-action.js claim namespace must equal api_identifier (${var.api_identifier})."
    }
  }
}

# Authoritative for the ENTIRE post-login flow: Actions not listed here are
# unbound on apply. Add future post-login Actions to this resource.
resource "auth0_trigger_actions" "post_login" {
  trigger = "post-login"

  actions {
    id           = auth0_action.stamp_profile_claims.id
    display_name = auth0_action.stamp_profile_claims.name
  }
}
