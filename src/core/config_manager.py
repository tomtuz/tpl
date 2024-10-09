import json
import os
import platform

from cryptography.fernet import Fernet


def get_config_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("USERPROFILE"), ".config", "tpl")
    else:
        return os.path.join(os.path.expanduser("~"), ".config", "tpl")


def ensure_config_dir():
    os.makedirs(get_config_dir(), exist_ok=True)


def load_config():
    config_file = os.path.join(get_config_dir(), "config.json")
    print(f"Load config: {config_file}")
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {}


def save_config(config):
    ensure_config_dir()
    config_file = os.path.join(get_config_dir(), "config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    print("save_config()")


def generate_key():
    return Fernet.generate_key()


def get_or_create_key():
    key_file = os.path.join(get_config_dir(), "encryption.key")
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = generate_key()
        ensure_config_dir()
        with open(key_file, "wb") as f:
            f.write(key)
        return key


def encrypt_value(value):
    key = get_or_create_key()
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()


def decrypt_value(value):
    key = get_or_create_key()
    f = Fernet(key)
    return f.decrypt(value.encode()).decode()


def get_config_value(key, default=None, sensitive=False):
    print(f"get_config_value({key})")

    config = load_config()
    print(f"Loaded config: {config}")

    keys = key.split(".")
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            value = default
            break

    print(f"Get (config) value: {value}")

    return decrypt_value(value) if sensitive and value is not None else value


def set_config_value(key, value, sensitive=False):
    print("set_config_value()")

    config = load_config()
    print(f"Loaded config: {config}")

    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    current[keys[-1]] = encrypt_value(value) if sensitive else value

    print(f"Set (config) value -> config: {config}")
    save_config(config)


def remove_config_value(key):
    config = load_config()
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            return
        current = current[k]
    if keys[-1] in current:
        del current[keys[-1]]
        save_config(config)


# # Example usage
# if __name__ == "__main__":
#     set_config_value("example_key", "example_value")
#     set_config_value("sensitive_key", "sensitive_value", sensitive=True)
#     print(get_config_value("example_key"))
#     print(get_config_value("sensitive_key", sensitive=True))
#     remove_config_value("example_key")
#     print(get_config_value("example_key", "default_value"))
