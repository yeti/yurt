variable "tenant_name" {
  description = "Human-readable name for this tenant (e.g. 'Staging')"
  type        = string
}

variable "app_url" {
  description = "Frontend application URL (e.g. https://staging-frontend.onrender.com)"
  type        = string
}

variable "api_identifier" {
  description = "Auth0 API audience identifier (e.g. __YURT_API_IDENTIFIER__)"
  type        = string
}

variable "additional_app_urls" {
  description = "Additional application base URLs without path (e.g. http://localhost:3000)"
  type        = list(string)
  default     = []
}
