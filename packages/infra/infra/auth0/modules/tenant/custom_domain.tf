# Custom domain for the tenant. Auth0 refuses to create one until the
# tenant has a credit card on file (verification only — the card is not
# charged), so both variables stay unset until then.
variable "custom_domain" {
  description = "Custom domain the tenant serves auth from (e.g. auth.example.com); null leaves the default *.auth0.com domain"
  type        = string
  default     = null
}

variable "verify_custom_domain" {
  description = "Flip to true only after the verification CNAME from the custom_domain_verification_records output exists in DNS"
  type        = bool
  default     = false
}

resource "auth0_custom_domain" "tenant" {
  count = var.custom_domain == null ? 0 : 1

  domain = var.custom_domain
  type   = "auth0_managed_certs"
}

# DNS is manual (registrar CNAME), so verification is a second apply: the
# first creates the domain and emits the record; this resource polls Auth0
# until the record resolves.
resource "auth0_custom_domain_verification" "tenant" {
  count = var.custom_domain != null && var.verify_custom_domain ? 1 : 0

  custom_domain_id = auth0_custom_domain.tenant[0].id

  timeouts {
    create = "15m"
  }
}
