#!/usr/bin/env python3

import os

from src.core import file_manager
from src.utils.helpers import get_file_index_path


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


def getFile(filename, variant="base", target_dir=None):
    if target_dir is None:
        target_dir = os.getcwd()

    print(f"[DEBUG] getFile called with: filename={filename}, variant={variant}, target_dir={target_dir}")

    file_index_path = get_file_index_path()
    print(f"[DEBUG] file_index_path: {file_index_path}")

    source_file = os.path.join(file_index_path, filename, f"{variant}.json")
    print(f"[DEBUG] Constructed source_file: {source_file}")

    print(f'"source": {source_file}')
    print(f'"target": {target_dir}')

    if not os.path.exists(source_file):
        print(f"[FAIL] '{filename}' file index doesn't exist.")
        print(f"[DEBUG] Checked path: {source_file}")
        return 1

    target_file = os.path.join(target_dir, f"{filename}_{variant}.json")
    print(f"[DEBUG] Constructed target_file: {target_file}")

    if file_manager.copy_file(source_file, target_file):
        print(f"[OK] Copied '{filename}' index to {target_file}")
        return 0
    else:
        print(f"[FAIL] to copy '{filename}' index")
        print(f"[DEBUG] Copy failed from {source_file} to {target_file}")
        return 1
