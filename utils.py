import json


def load_config(path):
    conf = None
    with open(path, "r") as f:
        conf = json.load(f)

    return _validate_config(conf)


def _validate_config(config):
    if "host" not in config or not isinstance(config.get("host"), str):
        raise ValueError("Config should contains key \'host\' with str value")

    if "port" not in config or not isinstance(config.get("port"), int):
        raise ValueError("Config should contains key \'port\' with int value")

    return config
