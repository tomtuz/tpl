import os

import yaml


class TemplateConfig:
    def __init__(
        self,
        name: str,
        description: str,
        files: list[str],
        variants: dict[str, list[str]] | None = None,
        post_actions: list[str] | None = None,
    ):
        self.name = name
        self.description = description
        self.files = files
        self.variants = variants or {}
        self.post_actions = post_actions or []

    @classmethod
    def from_yaml(cls, yaml_content: str) -> "TemplateConfig":
        data = yaml.safe_load(yaml_content)
        return cls(
            name=data["name"],
            description=data["description"],
            files=data["files"],
            variants=data.get("variants"),
            post_actions=data.get("post_actions"),
        )

    @classmethod
    def load_from_file(cls, file_path: str) -> "TemplateConfig":
        with open(file_path) as f:
            return cls.from_yaml(f.read())


def get_template_config(template_dir: str) -> TemplateConfig:
    config_path = os.path.join(template_dir, "template_config.yaml")
    if not os.path.exists(config_path):
        raise ValueError(f"Template configuration file not found in {template_dir}")
    return TemplateConfig.load_from_file(config_path)
