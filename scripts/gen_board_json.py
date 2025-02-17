#!/usr/bin/env python3
import json
import os
import argparse
import yml_reftag


def fetch_soc(ref, search_path):
    soc_yml = yml_reftag.load_yaml_file(str(os.path.join(search_path, ref.category, ref.resc)))
    soc_name = next(iter(soc_yml.keys()))
    return {
        'name': soc_name,
        'vendor': fetch_vendor(soc_yml[soc_name]['vendor'], search_path),
        'harts': soc_yml[soc_name]['harts'],
    }

def fetch_vendor(ref, search_path):
    vendor_yml = yml_reftag.load_yaml_file(str(os.path.join(search_path, ref.category, ref.resc)))
    vendor_name = next(iter(vendor_yml.keys()))
    return {
        'name': vendor_name,
        'homepage': vendor_yml[vendor_name]['homepage'],
    }

def main(args: argparse.Namespace):
    board_yml = yml_reftag.load_yaml_file(args.input_file)
    board_name = next(iter(board_yml.keys()))
    json_result = {
        'name': board_name,
        'vendor': fetch_vendor(board_yml[board_name]['vendor'], args.search_path),
        'soc': fetch_soc(board_yml[board_name]['soc'], args.search_path),
        'type': board_yml[board_name]['type'],
        'status': board_yml[board_name]['status'],
        'pictures': []
    }
    if 'pictures' in board_yml[board_name]:
        for pic_ref in board_yml[board_name]['pictures']:
            json_result['pictures'].append("%s/%s"%(pic_ref.category, pic_ref.resc))
    if 'hw_features' in board_yml[board_name]:
        json_result['hardware'] = {
            'ram': {
                'type': board_yml[board_name]['hw_features']['ram']['type'],
                'capacity': board_yml[board_name]['hw_features']['ram']['capacity'],
            },
            'storage': board_yml[board_name]['hw_features']['storage'],
            'connectivity': board_yml[board_name]['hw_features']['connectivity'],
        }
    json_result['os'] ={}
    with open(args.output_file, 'w') as fp:
        json.dump(json_result, fp, indent=2)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input_file", action='store',
                            help="YAML document to be parsed",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-o", "--output_file", action='store',
                            help="JSON document to be saved",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-s", "--search_path", action='store',
                            help="Search path for YAMLs being referenced",
                            required=False, type=str, default='.'
                            )
    main(arg_parser.parse_args())
