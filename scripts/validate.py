#!/usr/bin/env python3

import argparse
import yaml
import json
import cerberus
from cerberus import Validator
import sys

import yml_reftag


def main(args: argparse.Namespace):
    user_schema = yml_reftag.load_yaml_file(args.schema)
    # Fake a common root anchor to specify its schema
    schema = {
        '__root__': {
            'type': user_schema['__root__']['type'],
            'valuesrules': user_schema['__root__']
        },
    }
    validator = cerberus.Validator(schema)
    for ymlfile in args.input_file:
        yml = {'__root__': yml_reftag.load_yaml_file(ymlfile)}
        if not validator.validate(yml):
            raise Exception(json.dumps(validator.errors, indent=2))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--schema", action='store',
                            help="Schema to be validated against",
                            required=True, type=str,
                            )
    arg_parser.add_argument("input_file", action='store',
                            help="YAML documents to be validated",
                            nargs='+', type=str
                            )
    main(arg_parser.parse_args())
