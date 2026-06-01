def read_config(config_file_path = 'config.json'):
    import json

    with open(config_file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    return config["lamps"]

