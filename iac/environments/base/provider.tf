terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
  }
}

provider "google" {}

provider "google-beta" {}

provider "github" {
  owner = lookup(yamldecode(file(var.landscape_file)), "github_owner", null)
}
