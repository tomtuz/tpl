import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import file_manager

# Goal: Copy 'templates/poetry' template, Init the template.
# 1. Create 'test_project' folder. Validate.
# 2. Copy a file: 'source' to 'target'. Validate.
# 3. Get 'poetry' template path.
# 4. Copied 'poetry_template'.
# 5. Clean up

def test_file_operations():
    print("[TEST]: test_file_operations()")

    # Test creating a project directory
    test_project = "test_project"
    project_path = file_manager.create_project_directory(test_project)
    assert os.path.exists(project_path), f"Project directory {project_path} was not created"
    print(f"1. [OK] - Created folder at path: {project_path}")

    # Test copying a file
    source_file = os.path.join(os.path.dirname(__file__), "test_file.txt")
    with open(source_file, "w") as f:
        f.write("Test content")
    
    dest_file = os.path.join(project_path, "copied_file.txt")
    assert file_manager.copy_file(source_file, dest_file), "File copy failed"
    assert os.path.exists(dest_file), f"Destination file {dest_file} does not exist"
    print(f"2. [OK] - Copied file [source]/copied_file.txt to target: {project_path}")

    # Test getting template path
    template_path = file_manager.get_template_path("poetry")
    assert os.path.exists(template_path), f"Template path {template_path} does not exist"
    print(f"3. [OK] - Received path of template 'poetry': {project_path}")

    # Test copying template
    template_dest = os.path.join(project_path, "poetry_template")
    assert file_manager.copy_template("poetry", template_dest), "Template copy failed"
    assert os.path.exists(template_dest), f"Template destination {template_dest} does not exist"
    print("4. [OK] - Copied 'poetry_template':")
    print("[FROM]: [source]/poetry_template")
    print(f"[TO]: {template_dest}")

    # Clean up
    # shutil.rmtree(project_path)
    # os.remove(source_file)

    print("All file manager tests passed!")

if __name__ == "__main__":
    test_file_operations()
