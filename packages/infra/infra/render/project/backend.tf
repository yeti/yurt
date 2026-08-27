# HCP Terraform holds this root module's state (execution mode: Local — runs
# happen in CI or on a workstation; HCP stores state and locking only). To
# migrate to a different state backend later (e.g. AWS S3), swap this cloud
# block for a backend block here — state is configured per root module.
terraform {
  cloud {
    organization = "__YURT_HCP_ORG__"

    workspaces {
      name = "__YURT_PROJECT_SLUG__-render-project"
    }
  }
}
