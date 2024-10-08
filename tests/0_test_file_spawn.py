import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.commands import cmd_spawn 

CURRENT_PATH = os.getcwd()

# Goal: Copy file './src/file_index/central/index.json' template.
# 1. Copy a file: 'source' to 'target'. Validate.
# 2. Clean up

def test_file_spawn():
    print("[TEST]: test_file_spawn()")

    # > tpl spawn biome base 
    # cmd_spawn(target, filename, variant="base"):

    print(f"[DEBUG] CURRENT_PATH: {CURRENT_PATH}")
    cmd_spawn('central', 'base', CURRENT_PATH)
    cmd_spawn('central', CURRENT_PATH)
    cmd_spawn()

    # Clean up
    # shutil.rmtree(project_path)
    # os.remove(source_file)

    print("All file manager tests passed!")

if __name__ == "__main__":
    test_file_spawn()
