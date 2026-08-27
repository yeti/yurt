variable "name" {
  description = "Connection name (e.g. \"Username-Password-Authentication\")."
  type        = string
}

variable "strategy" {
  description = "Auth0 connection strategy (e.g. \"auth0\", \"google-oauth2\")."
  type        = string
}

variable "realms" {
  description = "Connection realms. Auth0 defaults to [name] when unset."
  type        = list(string)
  default     = null
}

variable "display_name" {
  description = "Optional display name shown on the login button."
  type        = string
  default     = null
}

variable "show_as_button" {
  description = "Whether the connection renders as a login button."
  type        = bool
  default     = null
}

variable "enabled_client_ids" {
  description = "Authoritative list of app client_ids this connection is enabled on. Required: pass an explicit empty list to disable the connection everywhere (omitting it is not allowed, so a connection cannot be disabled by accident)."
  type        = list(string)
}
