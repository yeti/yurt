terraform {
  required_version = ">= 1.10, < 2.0"

  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.3"
    }
  }
}
