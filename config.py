import yaml

def read_configuration(path):
    with open(path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)