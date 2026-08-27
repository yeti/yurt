resource "render_env_group" "backend" {
  name           = "${var.environment_name} Backend"
  environment_id = var.environment_id

  # env_vars and secret_files contain secrets and are managed via the Render
  # dashboard — Terraform owns only the group's existence and linkage.
  # environment_id is ignored because `terraform import` does not populate it
  # from the API; the server-side value already matches this config.
  lifecycle {
    ignore_changes = [
      env_vars,
      secret_files,
      environment_id,
    ]
  }
}

resource "render_env_group_link" "backend" {
  env_group_id = render_env_group.backend.id
  service_ids = [
    render_web_service.backend.id,
  ]
}
