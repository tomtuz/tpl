import json
import os
import platform
import re
from typing import Any

from cryptography.fernet import Fernet


def get_config_dir() -> str:
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("USERPROFILE", ""), ".config", "tpl")
    else:
        base_path = os.path.expanduser("~")
    return os.path.join(base_path, ".config", "tpl")


def ensure_config_dir() -> None:
    os.makedirs(get_config_dir(), exist_ok=True)


def load_config() -> dict[str, Any]:
    config_file = os.path.join(get_config_dir(), "config.json")
    if os.path.exists(config_file):
        with open(config_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict[str, Any]) -> None:
    ensure_config_dir()
    config_file = os.path.join(get_config_dir(), "config.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def generate_key() -> bytes:
    return Fernet.generate_key()


def get_or_create_key() -> bytes:
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


def encrypt_value(value: str) -> str:
    key = get_or_create_key()
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    key = get_or_create_key()
    f = Fernet(key)
    return f.decrypt(value.encode()).decode()


def validate_key(key: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_\.]+$", key))


def validate_value(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool, list, dict))


def get_config_value(key: str, default: Any = None, sensitive: bool = False) -> Any:
    if not validate_key(key):
        raise ValueError(f"Invalid key format: {key}")

    config = load_config()
    keys = key.split(".")
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            value = default
            break

    return decrypt_value(value) if sensitive and value is not None else value


def set_config_value(key: str, value: Any, sensitive: bool = False) -> None:
    if not validate_key(key):
        raise ValueError(f"Invalid key format: {key}")

    if not validate_value(value):
        raise ValueError(f"Invalid value type for key {key}")

    config = load_config()
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    current[keys[-1]] = encrypt_value(str(value)) if sensitive else value
    save_config(config)


def remove_config_value(key: str) -> None:
    if not validate_key(key):
        raise ValueError(f"Invalid key format: {key}")

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


def list_config_options() -> list[str]:
    def flatten_dict(d: dict[str, Any], prefix: str = "") -> list[str]:
        result = []
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                result.extend(flatten_dict(v, new_key))
            else:
                result.append(new_key)
        return result

    config = load_config()
    return flatten_dict(config)


# Example usage
if __name__ == "__main__":
    set_config_value("example_key", "example_value")
    set_config_value("sensitive_key", "sensitive_value", sensitive=True)
    print(get_config_value("example_key"))
    print(get_config_value("sensitive_key", sensitive=True))
    remove_config_value("example_key")
    print(get_config_value("example_key", "default_value"))
    print("Available config options:", list_config_options())
