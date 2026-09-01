resource "render_static_site" "frontend" {
  name           = "${var.environment_name} Frontend"
  repo_url       = var.repo_url
  build_command  = var.frontend_build_command
  branch         = var.branch
  auto_deploy    = var.auto_deploy
  publish_path   = "dist"
  root_directory = var.frontend_root_directory
  environment_id = var.environment_id

  custom_domains = length(var.frontend_custom_domains) > 0 ? var.frontend_custom_domains : null

  # SPA fallback: serve index.html for all client-side routes
  routes = [
    {
      source      = "/*"
      destination = "/index.html"
      type        = "rewrite"
    },
  ]

  # env_vars (VITE_* build-time vars) are managed via the Render dashboard
  lifecycle {
    ignore_changes = [
      env_vars,
    ]
  }
}
