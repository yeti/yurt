resource "render_web_service" "backend" {
  name              = "${var.environment_name} Backend"
  plan              = var.backend_plan
  region            = var.region
  environment_id    = var.environment_id
  root_directory    = var.backend_root_directory
  start_command     = var.backend_start_command
  health_check_path = var.backend_health_check_path
  num_instances     = 1

  custom_domains = length(var.backend_custom_domains) > 0 ? var.backend_custom_domains : null

  runtime_source = {
    native_runtime = {
      branch        = var.branch
      build_command = var.backend_build_command
      repo_url      = var.repo_url
      runtime       = "node"
      auto_deploy   = var.auto_deploy
    }
  }

  # env_vars contain secrets and are managed via the Render dashboard
  lifecycle {
    ignore_changes = [
      env_vars,
    ]
  }
}
