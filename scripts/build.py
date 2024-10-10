import os
import shutil
import subprocess


def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        exit(1)


def clean_old_builds():
    print("Cleaning old build artifacts...")
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    for file in os.listdir("."):
        if file.endswith(".whl") or file.endswith(".tar.gz"):
            os.remove(file)
    print("Old build artifacts removed.")


def build_package():
    print("Building package...")
    run_command("poetry build")


def copy_dist_files():
    print("Copying distribution files...")
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print(f"Error: {dist_dir} directory not found.")
        exit(1)
    try:
        for file in os.listdir(dist_dir):
            src = os.path.join(dist_dir, file)
            dst = os.path.join(".", file)
            shutil.copy2(src, dst)
        print("Distribution files copied to project root.")
    except Exception as e:
        print(f"Error copying distribution files: {str(e)}")
        exit(1)


def main():
    clean_old_builds()
    build_package()
    # copy_dist_files()
    print("Build process completed successfully.")


if __name__ == "__main__":
    main()
