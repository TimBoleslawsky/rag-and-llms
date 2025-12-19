from types import SimpleNamespace

import yaml


class ConfigHandler:
    @staticmethod
    def handle_config(args):
        # Load YAML configuration
        with open(args.config, 'r') as f:
            config_dict = yaml.safe_load(f)

        def dict_to_namespace(d):
            return SimpleNamespace(**{
                k: dict_to_namespace(v) if isinstance(v, dict) else v
                for k, v in d.items()
            })

        return dict_to_namespace(config_dict)
