from xia_module import Module


class Table(Module):
    module_name = "gcp-module-table"
    activate_depends = ["gcp-module-project"]
