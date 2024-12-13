import os
import shutil
import subprocess

DIST_DIR = "dist"


def run_command(command):
    print(f"\n3. [run_command({command})]...")
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        exit(1)


def clean_old_builds():
    print("\n1. Cleaning old build artifacts...")

    if not os.path.exists(DIST_DIR):
        print("Cleanup completed! (empty)")
        return

    print("[DEL] folder: [./dist]...")
    shutil.rmtree(DIST_DIR)

    for file in os.listdir("."):
        if file.endswith(".whl") or file.endswith(".tar.gz"):
            print(f"[DEL] file: [{file}]...")
            os.remove(file)

    print("Cleanup completed! (rem)")


def build_package():
    print("\n2. Building package...")
    run_command("poetry build")


def copy_dist_files():
    print("\n4. Copying distribution files...")

    if not os.path.exists(DIST_DIR):
        print(f"Error: {DIST_DIR} directory not found.")
        exit(1)

    try:
        for file in os.listdir(DIST_DIR):
            src = os.path.join(DIST_DIR, file)
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
