locals {
  modules = yamldecode(file(var.modules_file))
}