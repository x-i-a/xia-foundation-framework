import re
import os
import shutil
import subprocess
import importlib
import yaml
from gcp_framework.framework import Framework


class Foundation(Framework):
    def __init__(self, config_dir: str = "config", **kwargs):
        self.config_dir = config_dir
        self.module_dir = os.path.sep.join(["iac", "modules"])
        self.env_dir = os.path.sep.join(["iac", "environments"])
        self.landscape_yaml = os.path.sep.join([self.config_dir, "landscape.yaml"])
        self.application_yaml = os.path.sep.join([self.config_dir, "applications.yaml"])
        self.module_yaml = os.path.sep.join([self.config_dir, "modules.yaml"])

        # Temporary files
        self.requirements_txt = os.path.sep.join([self.config_dir, "requirements.txt"])
        self.package_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')

    def bigbang(self, cosmos_name: str, realm_name: str = None):
        """Create the realm administration project

        TODO:
            * Activate Cloud Billing API during cosmos project creation
            * Activate Cloud Resource Manager API during cosmos project creation
            * Activate Identity and Access Management during cosmos project creation
        """

        with open(self.landscape_yaml, 'r') as file:
            landscape_dict = yaml.safe_load(file) or {}
        current_settings = landscape_dict.get("settings", {})
        current_cosmos_name = current_settings.get("cosmos_name", "")
        if not cosmos_name:
            raise ValueError("Realm project must be provided")
        if current_cosmos_name and current_cosmos_name != cosmos_name:
            raise ValueError("Realm project doesn't match configured landscape.yaml")
        realm_name = cosmos_name if not realm_name else realm_name
        get_billing_cmd = f"gcloud billing accounts list --filter='open=true' --format='value(ACCOUNT_ID)' --limit=1"
        r = subprocess.run(get_billing_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        current_settings["billing_account"] = r.stdout if "ERROR" not in r.stderr else None
        print(current_settings["billing_account"])
        check_project_cmd = f"gcloud projects list --filter='{cosmos_name}' --format='value(projectId)'"
        r = subprocess.run(check_project_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if cosmos_name in r.stdout:
            print(f"Realm Project {cosmos_name} already exists")
        else:
            create_proj_cmd = f"gcloud projects create {cosmos_name} --name='{realm_name}'"
            r = subprocess.run(create_proj_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            if "ERROR" not in r.stderr:
                print(f"Realm Project {cosmos_name} create successfully")
                current_settings["realm_name"] = realm_name
                current_settings["cosmos_name"] = cosmos_name
                with open(self.landscape_yaml, 'w') as file:
                    yaml.dump(landscape_dict, file, default_flow_style=False, sort_keys=False)
            else:
                print(r.stderr)

    def create_backend(self, foundation_name: str):
        with open(self.landscape_yaml, 'r') as file:
            landscape_dict = yaml.safe_load(file) or {}
        current_settings = landscape_dict.get("settings", {})
        if not current_settings.get("cosmos_name", ""):
            raise ValueError("Cosmos Name must be defined")
        if not foundation_name:
            raise ValueError("Foundation name must be provided")
        bucket_name = current_settings["realm_name"] + "_" + foundation_name
        foundation_region = current_settings.get("foundation_region", "eu")
        bucket_project = current_settings['cosmos_name']
        check_bucket_cmd = f"gsutil ls -b gs://{bucket_name}"
        r = subprocess.run(check_bucket_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if "AccessDeniedException" not in r.stderr and "NotFound" not in r.stderr:
            print(f"Bucket {bucket_name} already exists")
        else:
            create_bucket_cmd = f"gsutil mb -l {foundation_region} -p {bucket_project} gs://{bucket_name}/"
            r = subprocess.run(create_bucket_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            if "ERROR" not in r.stderr:
                print(f"Bucket {bucket_name} create successfully")
                current_settings["foundation_name"] = foundation_name
                if not current_settings.get("project_prefix", ""):
                    current_settings["project_prefix"] = foundation_name + "-"
                with open(self.landscape_yaml, 'w') as file:
                    yaml.dump(landscape_dict, file, default_flow_style=False, sort_keys=False)
            else:
                print(r.stderr)

    def terraform_init(self, env: str):
        with open(self.landscape_yaml, 'r') as file:
            landscape_dict = yaml.safe_load(file) or {}
        current_settings = landscape_dict.get("settings", {})
        bucket_name = current_settings["realm_name"] + "_" + current_settings["foundation_name"]
        tf_init_cmd = f'terraform -chdir=iac/environments/{env} init -backend-config="bucket={bucket_name}"'
        subprocess.run(tf_init_cmd, shell=True)

    def terraform_apply(self, env: str):
        tf_apply_cmd = f'terraform -chdir=iac/environments/{env} apply'
        subprocess.run(tf_apply_cmd, shell=True)

    def terraform_plan(self, env: str):
        tf_plan_cmd = f'terraform -chdir=iac/environments/{env} plan'
        subprocess.run(tf_plan_cmd, shell=True)

    def birth(self, foundation_name: str):
        """"""
        self.create_backend(foundation_name)
        # self.terraform_init('prd')
        # self.register_module("gcp-module-project", "Project")
        # self.register_module("gcp-module-application", "Application")
        # self.update_requirements()
        # self.install_requirements()
        # self.enable_modules()

    def prepare(self, skip_terraform: bool = False):
        self.update_requirements()
        self.install_requirements()
        self.load_modules()
        self.enable_environments("prd")
        if not skip_terraform:
            self.terraform_init("prd")
            self.terraform_plan("prd")

    def register_module(self, module_name: str, package: str, module_class: str):
        if not self.package_pattern.match(package):
            return ValueError("Package name doesn't meet the required pattern")

        with open(self.module_yaml, 'r') as file:
            module_dict = yaml.safe_load(file) or {}

        if module_name in module_dict:
            print(f"Module {module_name} already exists")
        else:
            module_dict[module_name] = {"package": package, "class": module_class}
            print(f"Module {module_name} Registered")

        with open(self.module_yaml, 'w') as file:
            yaml.dump(module_dict, file, default_flow_style=False, sort_keys=False)

    def update_requirements(self):
        with open(self.module_yaml, 'r') as file:
            module_dict = yaml.safe_load(file) or {}
        all_packages = [module_config["package"] for module_name, module_config in module_dict.items()]
        all_packages = list(set(all_packages))
        package_list = []

        for package_name in all_packages:
            module_name = package_name.replace("-", "_")
            if os.path.exists(f"./{module_name}"):
                print(f"Found local package {package_name}: ./{module_name}")
            elif os.path.exists(f"../{package_name}"):
                print(f"Found local package {package_name}: ../{package_name}")
            else:
                package_list.append(package_name)
                print(f"{package_name} added to requirements")


        requirements_content = "\n".join(package_list)
        with open(self.requirements_txt, 'w') as file:
            file.write(requirements_content)

    def install_requirements(self):
        with open(self.landscape_yaml, 'r') as file:
            landscape_dict = yaml.safe_load(file) or {}
        pip_index_url = landscape_dict["settings"].get("pip_index_url", "https://pypi.org/simple")
        subprocess.run(['pip', 'install', '-r', self.requirements_txt,
                        f"--index-url={pip_index_url}"], check=True)

    def load_modules(self):
        with open(self.module_yaml, 'r') as file:
            module_dict = yaml.safe_load(file) or {}
        for module_name, module_config in module_dict.items():
            module_obj = importlib.import_module(module_config["package"].replace("-", "_"))
            module_class = getattr(module_obj, module_config["class"])
            module_instance = module_class()
            for event, event_cfg in module_config.get("events", {}).items():
                event_cfg = {} if not event_cfg else event_cfg
                if event == "deploy":
                    module_instance.enable(self.module_dir, **event_cfg)
                elif event == "activate":
                    module_instance.activate(self.module_dir, **event_cfg)

    def enable_environments(self, env: str):
        if os.path.exists(os.path.join(self.env_dir, env)):
            print(f"Local environment {env} found")
        else:
            shutil.copytree(os.path.join(self.env_dir, "base"), os.path.join(self.env_dir, env))

    def init_module(self, module_name: str, package: str, module_class: str):
        self.register_module(module_name, package, module_class)
        self.update_requirements()
        self.install_requirements()

    def create_app(self, app_name: str):
        print(f"Creating application: {app_name}")

