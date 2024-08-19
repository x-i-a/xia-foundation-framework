terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
  }
}

provider "github" {
  owner = lookup(yamldecode(file(var.landscape_file))["settings"], "github_owner", null)
}

provider "google" {}

provider "google-beta" {}

