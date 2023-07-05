from pathlib import Path

import yaml

# Path of default config file
CONFIG_PATH = Path(__file__).parent / "default_config.yml"

# Read the default config file
if Path(CONFIG_PATH).is_file():
    with open(CONFIG_PATH, "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
else:
    raise FileNotFoundError(f"{CONFIG_PATH} not found. Please create one.")
