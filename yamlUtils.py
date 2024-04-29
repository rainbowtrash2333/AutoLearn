import yaml


def _read_yaml_config(file_path='config.yaml'):
    with open(file_path, 'r', encoding='utf-8') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            return None


class Config:
    _config = _read_yaml_config()

    @classmethod
    def get_config(cls):
        if not cls._config:
            cls._instance = cls()
        return cls._config


if __name__ == '__main__':
    print(Config.get_config()['Learn_Cbit'])
