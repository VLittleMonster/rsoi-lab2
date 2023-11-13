from yaml import safe_load


def get_settings(config_file_name: str = "./app/config/config.yaml", service_config_name: str = 'reservation_app'):
    with open(config_file_name) as file:
        data = safe_load(file)
    return data[service_config_name]


def get_db_url(config_file_name: str = "./app/config/config.yaml"):
    settings = get_settings(config_file_name, service_config_name='postgres_db')

    return f"postgresql://{settings['user']}:" \
                        f"{settings['password']}@" \
                        f"{settings['host']}:" \
                        f"{settings['port']}/" \
                        f"{settings['db_name']}"
