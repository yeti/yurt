# Terraform IaC bootstrap app — Management API grant.
#
# The grant, its scope list, and the lockout/rollout rationale live in
# `modules/iac-grant`. This file is just the per-tenant flag plumbed through.

variable "manage_iac_grant" {
  description = "Manage the Terraform IaC app's Management API grant in Terraform. Enable only after importing this tenant's existing grant (see infra/README.md)."
  type        = bool
  default     = false
}

module "iac_grant" {
  source           = "../iac-grant"
  manage_iac_grant = var.manage_iac_grant
}
