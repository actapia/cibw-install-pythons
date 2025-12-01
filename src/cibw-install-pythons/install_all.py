import tempfile
import argparse
import inspect
import os
import shutil
import sys
from pathlib import Path
from platform import machine
from filelock import FileLock

from cibuildwheel.platforms import macos as platform
from cibuildwheel.util import resources
from cibuildwheel.util.cmd import call
from cibuildwheel.util.file import CIBW_CACHE_PATH, download
from cibuildwheel.ci import detect_ci_provider
from cibuildwheel import errors

def handle_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    macos_parser = subparsers.add_parser("macos")
    return parser.parse_args()

def macos_install():
    configs = platform.all_python_configurations()
    with tempfile.TemporaryDirectory() as tmp_root:
        for config in configs:
            arch = "_".join(config.identifier.split("-")[-1].split("_")[1:])
            if arch == machine():
                print("Installing", config.identifier)
                tmp = Path(tmp_root) / config.identifier
                tmp.mkdir(exist_ok=True)
                implementation_id = config.identifier.split("-")[0]
                if implementation_id.startswith("cp"):
                    free_threading = "t-macos" in config.identifier
                    base_python = platform.install_cpython(
                        tmp,
                        config.version,
                        config.url,
                        free_threading
                    )
                elif implementation_id.startswith("pp"):
                    base_python = platform.install_pypy(tmp, config.url)
                elif implementation_id.startswith("gp"):
                    base_python = platform.install_graalpy(tmp, config.url)    

def main():
    args = handle_arguments()
    if args.command == "macos":
        macos_install()
 

if __name__ == "__main__":
    main()
