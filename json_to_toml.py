# convert credentials.jsoon file to TOML format
# Usage: python json_to_toml.py

import json
import toml

with open('credentials.json') as json_file:
    data = json.load(json_file)
    toml_data = toml.dumps(data)
    print(toml_data)
    with open('credentials.toml', 'w') as toml_file:
        toml_file.write(toml_data)
