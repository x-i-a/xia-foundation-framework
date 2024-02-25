terraform {
  required_providers {
    github = {
      source  = "integrations/github"
    }
  }
}

locals {
  landscape = yamldecode(file(var.landscape_file))
  applications = yamldecode(file(var.applications_file))
  environment_dict = local.landscape["environments"]
}

locals {
  all_pool_settings = toset(flatten([
    for app_name, app in local.applications : [
      for env_name, env in local.environment_dict : {
        app_name          = app_name
        env_name          = env_name
        repository_owner  = app["repository_owner"]
        repository_name   = app["repository_name"]
        match_branch      = env["match_branch"]
      }
    ]
  ]))
}

locals {
  all_review_users = toset(flatten([
    for app_name, app in local.applications : [
      for env_name, env in local.environment_dict : {
        app_name          = app_name
        env_name          = env_name
        user_names        = lookup(env, "review_users", [])
      }
    ]
  ]))
}

locals {
  all_review_teams = toset(flatten([
    for app_name, app in local.applications : [
      for env_name, env in local.environment_dict : [
        for team_name in lookup(env, "review_teams", []): {
          app_name          = app_name
          env_name          = env_name
          team_name         = team_name
        }
      ]
    ]
  ]))
}

provider "github" {
  owner = "x-i-a"
}

data "github_users" "review_users" {
  for_each = { for s in local.all_review_users : "${s.app_name}-${s.env_name}" => s if length(s.user_names) > 0}

  usernames = each.value["user_names"]
}

resource "github_repository" "app-repository" {
  for_each = local.applications

  name        = each.value["repository_name"]
  description = "Application: ${each.value["repository_name"]}"
  is_template = lookup(each.value, "is_template", false)

  visibility = each.value["visibility"]

  template {
    owner                = each.value["template_owner"]
    repository           = each.value["template_name"]
  }
}

resource "github_repository_environment" "action_environments" {
  for_each = { for s in local.all_pool_settings : "${s.app_name}-${s.env_name}" => s }

  environment         = each.value["env_name"]
  repository          = each.value["repository_name"]

  wait_timer          = lookup(local.environment_dict[each.value["env_name"]], "wait_timer", null)

  reviewers {
    users = lookup(data.github_users.review_users, each.key, {node_ids = []}).node_ids
  }

  depends_on = [github_repository.app-repository]
}
