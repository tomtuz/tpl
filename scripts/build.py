import shutil
import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode())
        exit(1)
    return output.decode()

def main():
    # Install dependencies
    print("Installing dependencies...")
    run_command("poetry install")

    # Build executable
    print("Building executable...")
    run_command("poetry run pyinstaller --name=tpl --onefile src/main.py")

    # Copy templates
    print("Copying templates...")
    shutil.copytree("src/templates", "dist/templates", dirs_exist_ok=True)

    print("Build complete. Executable is located in the 'dist' directory.")

if __name__ == "__main__":
    main()
