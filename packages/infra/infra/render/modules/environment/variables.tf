variable "environment_name" {
  description = "Human-readable name for this environment (e.g. 'Staging', 'Production')"
  type        = string
}

variable "environment_id" {
  description = "Render environment ID (evm-...), minted by the project root module"
  type        = string
}

variable "region" {
  description = "Render region (e.g. 'oregon')"
  type        = string
}

variable "branch" {
  description = "Git branch to deploy from"
  type        = string
}

variable "repo_url" {
  description = "GitHub repository URL for both services"
  type        = string
}

variable "auto_deploy" {
  description = "Enable automatic deploys on git push"
  type        = bool
  default     = true
}

# Backend overrides

variable "backend_plan" {
  description = "Render plan for the backend web service"
  type        = string
  default     = "starter"
}

variable "backend_root_directory" {
  description = "Monorepo path of the backend package"
  type        = string
  default     = "packages/backend"
}

variable "backend_build_command" {
  description = "Backend build command (the package's build script runs install, prisma generate, tsc, resolve-tspaths, and prisma migrate deploy)"
  type        = string
  default     = "pnpm build"
}

variable "backend_start_command" {
  description = "Backend start command (the package has no start script; ESM entry compiled by tsc)"
  type        = string
  default     = "node dist/src/server.js"
}

variable "backend_health_check_path" {
  description = "Health check endpoint path (empty string to disable)"
  type        = string
  default     = "/healthz"
}

# Frontend overrides

variable "frontend_root_directory" {
  description = "Monorepo path of the frontend package"
  type        = string
  default     = "packages/frontend"
}

variable "frontend_build_command" {
  description = "Build command for the static site (static-site build images lack pnpm, so install it explicitly)"
  type        = string
  default     = "npm install -g pnpm@10 && pnpm install && pnpm build"
}

# Database overrides

variable "database_name" {
  description = "PostgreSQL database name"
  type        = string
}

variable "database_user" {
  description = "PostgreSQL database user"
  type        = string
}

variable "database_plan" {
  description = "Render plan for the PostgreSQL instance"
  type        = string
  default     = "basic_256mb"
}

variable "database_version" {
  description = "PostgreSQL major version"
  type        = string
  default     = "18"
}

variable "database_disk_size_gb" {
  description = "Disk size in GB for the PostgreSQL instance"
  type        = number
  default     = 1
}

variable "database_high_availability" {
  description = "Enable high availability for the PostgreSQL instance"
  type        = bool
  default     = false
}

variable "database_ip_allow_list" {
  description = "IP allow list for the PostgreSQL instance (empty = internal-only access)"
  type = set(object({
    cidr_block  = string
    description = string
  }))
  default = []
}

# Custom domains (unused in staging; ready for prod)

variable "frontend_custom_domains" {
  description = "Custom domain names for the static site frontend"
  type = set(object({
    name = string
  }))
  default = []
}

variable "backend_custom_domains" {
  description = "Custom domain names for the backend web service"
  type = set(object({
    name = string
  }))
  default = []
}
