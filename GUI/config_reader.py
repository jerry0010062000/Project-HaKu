import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data

# 示例用法
config = load_config('config.json')
print(config['database']['host'])
print(config['api_key'])
