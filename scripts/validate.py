#!/usr/bin/env python3

import argparse
import yaml
import json
import cerberus
from cerberus import Validator
import sys
import os

import yml_helper


class FileReferenceValidator(Validator):
    types_mapping = Validator.types_mapping.copy()
    types_mapping['file_reference'] = cerberus.TypeDefinition('file_reference', (yml_helper.FileReference,), ())

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self.current_document = kwargs.get("current_document")
        self.base_path = kwargs.get("base_path")

    def _check_with_file_exist(self, field, value):
        if os.path.isabs(value.path):
            target_file = os.path.normpath(self.base_path + value.path)
        else:
            curr_file_dir = os.path.dirname(self.current_document)
            if os.path.normpath("/rootguard" + curr_file_dir + os.path.sep + value.path) != os.path.normpath("/rootguard" + os.path.normpath(curr_file_dir + os.path.sep + value.path)):
                raise Exception("Relative path exceeding root directory")
            else:
                target_file = os.path.normpath("." + curr_file_dir + os.path.sep + value.path)
        if not os.path.isfile(target_file):
            self._error(field, "\'%s\' must be an existing file"%(target_file))


def main(args: argparse.Namespace):
    schemafile = args.schema
    if not os.path.isabs(schemafile):
        schemafile = os.path.normpath(os.path.sep + schemafile)
    user_schema = yml_helper.load_yaml_file(schemafile, base_path=args.root)

    for ymlfile in args.input_file:
        if not os.path.isabs(ymlfile):
            ymlfile = os.path.normpath(os.path.sep + ymlfile)
        validator = FileReferenceValidator(current_document=ymlfile, base_path=args.root)
        yml = {'__root__': yml_helper.load_yaml_file(ymlfile, args.root)}
        if not validator.validate(yml, user_schema):
            raise Exception("While processing %s:\n%s"%(ymlfile, json.dumps(validator.errors, indent=2)))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--schema", action='store',
                            help="Schema to be validated against",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-r", "--root", action='store',
                            help="Root directory for path lookup",
                            default=".", type=str,
                            )
    arg_parser.add_argument("input_file", action='store',
                            help="YAML documents to be validated, resolved based on --root",
                            nargs='+', type=str
                            )
    main(arg_parser.parse_args())
