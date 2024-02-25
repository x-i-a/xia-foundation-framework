module "gh_module_application" {
  source = "../../modules/gh-module-application"

  landscape_file = "../../../config/landscape.yaml"
  applications_file = "../../../config/applications.yaml"
}
