
import os
from pathlib import Path
from dynaconf import Dynaconf

# settings = Dynaconf(
#     envvar_prefix="DYNACONF",
#     settings_files=['settings.toml', '.secrets.toml'],
# )

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.


# get current file location, then add settings.toml and .secrets.toml
cwd = os.path.dirname(os.path.realpath(__file__))
settings_files = []
potential_file_names = ["settings.toml", ".secrets.toml", ".env"]

home_dir = Path(os.path.expanduser("~"))

dirs_to_search = [cwd, os.path.join(cwd, ".."), os.path.join(cwd, "..", "..")]

for potential_file_name in potential_file_names:
    for d in dirs_to_search:
        file = os.path.join(d, potential_file_name)
        # test if the file exists
        if os.path.exists(file):
            settings_files.append(file)

for f in settings_files:
    # get the file name
    file_name = os.path.basename(f)
    if file_name == ".secrets.toml":
        break
        
# print("settings_files: ", settings_files)
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=settings_files,
)

