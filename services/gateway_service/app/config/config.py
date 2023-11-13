from yaml import safe_load


def get_settings(config_file_name: str = "./app/config/config.yaml", service_config_name: str = 'gateway_app'):
    with open(config_file_name) as file:
        data = safe_load(file)
    return data[service_config_name]
