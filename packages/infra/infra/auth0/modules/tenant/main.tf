terraform {
  required_version = ">= 1.10, < 2.0"

  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.41"
    }
  }
}
