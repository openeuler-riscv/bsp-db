#!/usr/bin/env python3
import json
import os
import argparse
from yml_helper import load_yaml_file


def fetch_soc(ref, base_path):
    soc_yml = load_yaml_file(ref.path, base_path=base_path)
    soc_name = next(iter(soc_yml.keys()))
    return {
        'name': soc_name,
        'vendor': fetch_vendor(soc_yml[soc_name]['vendor'], base_path=base_path),
    }

def fetch_vendor(ref, base_path):
    vendor_yml = load_yaml_file(ref.path, base_path=base_path)
    return {
        'name': vendor_yml['name'],
        'homepage': vendor_yml['homepage'],
    }

def main(args: argparse.Namespace):
    board_yml = load_yaml_file(args.input_file, base_path=args.root)

    board_name = next(iter(board_yml.keys()))
    json_result = dict()

    json_result["name"] = board_name
    json_result["vendor"] = fetch_vendor(board_yml[board_name]['vendor'], args.root)
    json_result["soc"] = fetch_soc(board_yml[board_name]['soc'], args.root)
    json_result["type"] = board_yml[board_name]['type']
    json_result["pictures"] = []
    if 'pictures' in board_yml[board_name]:
        for pic_ref in board_yml[board_name]['pictures']:
            json_result['pictures'].append(os.path.normpath(args.prefix + pic_ref.path))
    if 'hw_info' in board_yml[board_name]:
        json_result['hw_info'] = {}
        json_result['hw_info']["ram"] = {
            'type': board_yml[board_name]['hw_info']['ram']['type'],
            'capacity': board_yml[board_name]['hw_info']['ram']['capacity'],
        },
        json_result['hw_info']["storage"] = board_yml[board_name]['hw_info']['storage']
        json_result['hw_info']["connectivity"] = board_yml[board_name]['hw_info']['connectivity']
        json_result['hw_info']["peripheral"] = board_yml[board_name]['hw_info']['peripheral']
    json_result['imagesuites'] = []

    with open(args.output_file, 'w') as fp:
        json.dump(json_result, fp, indent=2)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input_file", action='store',
                            help="YAML document to be parsed, resolved based on --root",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-o", "--output_file", action='store',
                            help="JSON document to be saved",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-r", "--root", action='store',
                            help="Root directory for path lookup",
                            default=".", type=str,
                            )
    arg_parser.add_argument("-p", "--prefix", action='store',
                            help="URL prefix for resources",
                            default=".", type=str,
                            )
    main(arg_parser.parse_args())
