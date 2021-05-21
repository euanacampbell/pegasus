# test_capitalize.py

from configs.config import Config

config=Config()

def test_module_configs():  
    # config loads a value
    expected_result='something'
    load = config.mod_config['module']['val1']
    if load != expected_result:
        raise Exception(f"equals {expected_result} and not {load}")



