terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
  }
}

provider "google" {}

provider "google-beta" {}
