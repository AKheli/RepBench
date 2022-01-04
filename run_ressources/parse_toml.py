import toml
import os

def load_toml_file(filename="algos.toml"):
    if not filename.endswith("toml"):
        filename = f'{filename}.toml'

    parsed_toml = toml.load(f'{os.path.dirname(os.path.abspath(__file__))}/{filename}')
    print(parsed_toml)
    return parsed_toml