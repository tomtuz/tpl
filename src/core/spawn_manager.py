import logging
import os
import shutil

from src.core.template_config import TemplateConfig, get_template_config
from src.core.utils import get_script_dir

logger = logging.getLogger(__name__)


def get_template_dir(template_name: str) -> str:
    script_dir = get_script_dir()
    return os.path.normpath(os.path.join(script_dir, "templates", template_name))


def list_templates() -> list[str]:
    script_dir = get_script_dir()
    templates_dir = os.path.normpath(os.path.join(script_dir, "templates"))
    return [d for d in os.listdir(templates_dir) if os.path.isdir(os.path.join(templates_dir, d))]


def spawn_file(template_name: str, filename: str, variant: str | None = None) -> None:
    template_dir = get_template_dir(template_name)
    config = get_template_config(template_dir)

    if filename not in config.files:
        raise ValueError(f"File '{filename}' is not defined in the template configuration.")

    if variant and (variant not in config.variants or filename not in config.variants[variant]):
        raise ValueError(f"Variant '{variant}' for file '{filename}' is not defined in the template configuration.")

    source_file = os.path.normpath(os.path.join(template_dir, filename))
    if variant:
        source_file = f"{source_file}.{variant}"

    if not os.path.exists(source_file):
        raise ValueError(f"Source file '{source_file}' not found in template '{template_name}'.")

    destination_file = os.path.normpath(os.path.join(os.getcwd(), filename))

    if os.path.exists(destination_file):
        raise ValueError(f"File '{filename}' already exists in the current directory.")

    shutil.copy2(source_file, destination_file)
    logger.info(f"File '{filename}' spawned successfully from template '{template_name}'.")

    _run_post_actions(config, template_dir)


def spawn_project(template_name: str, project_name: str) -> None:
    template_dir = get_template_dir(template_name)
    config = get_template_config(template_dir)

    destination_dir = os.path.normpath(os.path.join(os.getcwd(), project_name))

    if os.path.exists(destination_dir):
        raise ValueError(f"Directory '{project_name}' already exists in the current directory.")

    os.makedirs(destination_dir)

    for file in config.files:
        source_file = os.path.normpath(os.path.join(template_dir, file))
        dest_file = os.path.normpath(os.path.join(destination_dir, file))
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(source_file, dest_file)

    logger.info(f"Project '{project_name}' spawned successfully from template '{template_name}'.")

    _run_post_actions(config, destination_dir)


def _run_post_actions(config: TemplateConfig, target_dir: str) -> None:
    for action in config.post_actions:
        try:
            # The logic to run each post-action
            # shell commands, Python scripts, etc.
            logger.info(f"Running post-action: {action}")
            # Example: os.system(f"cd {target_dir} && {action}")
        except Exception as e:
            logger.error(f"Error running post-action '{action}': {str(e)}")
