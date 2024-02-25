import os
import subprocess
import yaml


class Framework:
    def __init__(self, config_dir: str = "config", **kwargs):
        self.config_dir = config_dir
        self.landscape_yaml = os.path.sep.join([self.config_dir, "landscape.yaml"])

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