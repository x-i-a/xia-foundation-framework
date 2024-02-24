module "gcp_module_project" {
  source = "../../modules/gcp-module-project"

  landscape_file = "../../../config/landscape.yaml"
  applications_file = "../../../config/applications.yaml"
}
