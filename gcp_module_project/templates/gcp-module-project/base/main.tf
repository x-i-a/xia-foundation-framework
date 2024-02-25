module "gcp_module_project" {
  source = "../../modules/gcp-module-project"

  config_file = "../../../config/gcp-project.yaml"
  landscape_file = "../../../config/landscape.yaml"
  applications_file = "../../../config/applications.yaml"
}
