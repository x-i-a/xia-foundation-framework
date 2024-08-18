locals {
  landscape = yamldecode(file(var.landscape_file))
  applications = yamldecode(file(var.applications_file))
  modules = yamldecode(file(var.modules_file))
  environment_dict = lookup(local.landscape, "environments", {})
}

locals {
  app_env_config = toset(flatten([
    for app_name, app in local.applications : [
      for env_name, env in local.environment_dict : {
        app_name          = app_name
        env_name          = env_name
        repository_owner  = app["repository_owner"]
        repository_name   = app["repository_name"]
        match_branch      = env["match_branch"]
        match_event       = lookup(env, "match_event", "push")
      }
    ]
  ]))
}