locals {
  project = yamldecode(file(var.project_file))
  landscape = yamldecode(file(var.landscape_file))
  applications = yamldecode(file(var.applications_file))
  settings = lookup(local.landscape, "settings", {})
  cosmos_name = local.settings["cosmos_name"]
  realm_name = local.settings["realm_name"]
  foundation_name = local.settings["foundation_name"]
  tf_bucket_name = lookup(local.settings, "cosmos_name")
  folder_id = lookup(local.project, "folder_id", null)
  project_prefix = local.project["project_prefix"]
  billing_account = local.project["billing_account"]
  environment_dict = local.landscape["environments"]
  activated_apps = lookup(lookup(local.landscape["modules"], "gcp-module-project", {}), "applications", [])
}