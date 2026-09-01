resource "render_postgres" "database" {
  name                      = "${var.environment_name} Database"
  plan                      = var.database_plan
  region                    = var.region
  version                   = var.database_version
  database_name             = var.database_name
  database_user             = var.database_user
  disk_size_gb              = var.database_disk_size_gb
  environment_id            = var.environment_id
  high_availability_enabled = var.database_high_availability
  ip_allow_list             = var.database_ip_allow_list
}
