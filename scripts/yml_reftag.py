import yaml
import cerberus
from cerberus import Validator

class Reference(yaml.YAMLObject):
    yaml_tag = u'!ref'
    yaml_loader = yaml.SafeLoader
    def __init__(self, resc, category):
        self.resc = resc
        self.category = category

Validator.types_mapping['reference'] = cerberus.TypeDefinition('reference', (Reference,), ())

def load_yaml_file(filename: str):
    with open(filename, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            raise
