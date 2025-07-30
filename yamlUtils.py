from typing import Dict, Any, Optional

import yaml


def _read_yaml_config(file_path: str = 'config.yaml') -> Optional[Dict[str, Any]]:
    """Read YAML configuration file
    
    Args:
        file_path: Path to the YAML configuration file
        
    Returns:
        Configuration dictionary or None if failed to load
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as stream:
            config = yaml.safe_load(stream)
            return config
    except FileNotFoundError:
        print(f"Configuration file not found: {file_path}")
        return None
    except yaml.YAMLError as exc:
        print(f"YAML parsing error: {exc}")
        return None
    except Exception as exc:
        print(f"Unexpected error reading config: {exc}")
        return None


class Config:
    """Configuration manager using singleton pattern"""
    _config: Optional[Dict[str, Any]] = _read_yaml_config()

    @classmethod
    def get_config(cls) -> Optional[Dict[str, Any]]:
        """Get configuration dictionary
        
        Returns:
            Configuration dictionary or None if not loaded
        """
        if cls._config is None:
            cls._config = _read_yaml_config()
        return cls._config


if __name__ == '__main__':
    config = Config.get_config()
    if config:
        print(config.get('Learn_Cbit', 'Learn_Cbit section not found'))
    else:
        print("Failed to load configuration")
