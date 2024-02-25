from xia_module import Module


class Dataset(Module):
    module_name = "gcp-module-dataset"
    activate_depends = ["gcp-module-project"]
