import json
import subprocess


def run_command(command):
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error message: {process.stderr}")
        return None
    return process.stdout


def get_outdated_packages():
    output = run_command("poetry show --outdated --format json")
    if output is None:
        return []
    return json.loads(output)


def update_package(package):
    print(f"Updating {package['name']}...")
    result = run_command(f"poetry update {package['name']}")
    if result is None:
        return False
    return True


def run_tests():
    print("Running tests...")
    result = run_command("poetry run pytest")
    if result is None:
        return False
    return True


def main():
    outdated = get_outdated_packages()

    if not outdated:
        print("All packages are up to date.")
        return

    print(f"Found {len(outdated)} outdated package(s).")

    for package in outdated:
        print(f"\nUpdating {package['name']} from {package['version']} to {package['latest']}...")

        if not update_package(package):
            print(f"Failed to update {package['name']}. Skipping.")
            continue

        if not run_tests():
            print(f"Tests failed after updating {package['name']}. Reverting...")
            run_command(f"poetry add {package['name']}@{package['version']}")
            continue

        print(f"Successfully updated {package['name']} to {package['latest']}.")

    print("\nFinished updating packages.")


if __name__ == "__main__":
    main()
