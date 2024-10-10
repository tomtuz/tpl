import os
import platform
import shutil


def get_config_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("USERPROFILE"), ".config", "tpl")
    else:
        return os.path.join(os.path.expanduser("~"), ".config", "tpl")


def get_repos_dir():
    return os.path.join(get_config_dir(), "repos")


def ensure_dir(directory):
    os.makedirs(directory, exist_ok=True)


def copy_file(src, dest):
    try:
        shutil.copy2(src, dest)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False


def create_project_directory(project_name):
    folderPath = ""
    if platform.system() == "Windows":
        folderPath = os.path.join(os.environ.get("USERPROFILE"), ".config", "tpl", project_name)
    else:
        folderPath = os.path.join(os.path.expanduser("~"), ".config", "tpl", project_name)

    try:
        os.makedirs(folderPath, exist_ok=True)
        return folderPath
    except Exception as e:
        print(f"Error creating project directory: {e}")
        return None


def get_template_path(template_name):
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    return os.path.join(template_dir, template_name)


def copy_template(template_name, destination):
    template_path = get_template_path(template_name)
    if not os.path.exists(template_path):
        print(f"Template '{template_name}' not found.")
        return False

    try:
        shutil.copytree(template_path, destination)
        return True
    except Exception as e:
        print(f"Error copying template: {e}")
        return False


def get_repo_path(repo_name):
    return os.path.join(get_repos_dir(), repo_name)


def ensure_repo_dir(repo_name):
    repo_path = get_repo_path(repo_name)
    ensure_dir(repo_path)
    return repo_path
