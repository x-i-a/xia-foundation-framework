locals {
  landscape = yamldecode(file(var.landscape_file))
  applications = yamldecode(file(var.applications_file))
  modules = yamldecode(file(var.modules_file))
  environment_dict = lookup(local.landscape, "environments", {})
}

locals {
  # Get Activation App list for all Modules
  _dependency_flat = concat(
    flatten([
      for k, v in local.modules : [
        for p in lookup(v, "depends_on", []) : {
          apps    = lookup(v, "activate_scope", [])
          module = p
        } if length(lookup(v, "activate_scope", [])) > 0
      ]
    ]),
    flatten([
      for k, v in local.modules : {
        apps   = lookup(v, "activate_scope", [])
        module = k
      } if length(lookup(v, "activate_scope", [])) > 0
    ])
  )
  _dependency_grouped = { for item in local._dependency_flat : item.module => item.apps... }
  module_app_to_activate = { for k, v in local._dependency_grouped: k => tolist(toset(flatten(v)))}
}

locals {
  app_env_config = {
    for idx, pair in flatten([
      for app_name, app in local.applications : [
        for env_name, env in local.environment_dict : {
          app_name         = app_name
          env_name         = env_name
          match_branch     = env["match_branch"]
          match_event      = lookup(env, "match_event", "push")
        }
      ]
    ]) : "${pair.app_name}-${pair.env_name}" => {
      app_name         = pair.app_name
      env_name         = pair.env_name
      match_branch     = pair.match_branch
      match_event      = pair.match_event
    }
  }
}