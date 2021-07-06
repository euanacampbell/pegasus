import yaml

class Config:

    def __init__(self):
        self.env = {}
        self.mod_config = {}

        self.load_config_files()

    def load_config_files(self):
        
        with open("configs/setup.yaml", 'r') as file:
            try:
                self.env=yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        
        with open("configs/module_config.yaml", 'r') as file:
            try:
                self.mod_config=yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
    
    def get_module_config(self, module_name):

        try:
            self.mod_config[module_name]
        except KeyError:
            return(None)

if __name__ == "__main__":
    config = Config()

    print(config.map['command'])

