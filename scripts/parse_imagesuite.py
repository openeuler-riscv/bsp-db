#!/usr/bin/env python3
import argparse
import os.path
from filelock import FileLock
import yml_reftag
import json


def fetch_distro(ref, search_path):
    return yml_reftag.load_yaml_file(str(os.path.join(search_path, ref.category, ref.resc)))

def fetch_distro_with_rel(ref, search_path):
    distro_rel_yml = yml_reftag.load_yaml_file(str(os.path.join(search_path, ref.category, ref.resc)))
    distro_rel_name = next(iter(distro_rel_yml.keys()))
    distro = fetch_distro(distro_rel_yml[distro_rel_name]['belongs_to'], search_path)
    distro_rel = {
        'name': distro_rel_name,
        'imagesuites': []
    }
    return (
        distro, distro_rel
    )

def main(args: argparse.Namespace):
    img_yml = yml_reftag.load_yaml_file(args.input_file)
    img_name = next(iter(img_yml.keys()))

    distro, distro_release = fetch_distro_with_rel(img_yml[img_name]['belongs_to'], args.search_path)
    distro_name = next(iter(distro.keys()))

    doc_urls = []
    if 'docs' in img_yml[img_name]:
        for doc in img_yml[img_name]['docs']:
            doc_urls.append("%s/%s"%(doc.category, doc.resc))

    img_json = {
        'name': img_name,
        'kernel': img_yml[img_name]['kernel'],
        'userspace': img_yml[img_name]['userspace'],
        'isa': img_yml[img_name]['isa'],
        'type': img_yml[img_name]['type'],
        'features': img_yml[img_name]['features'],
        'files': img_yml[img_name]['files'],
        'docs': doc_urls,
    }
    for board_ref in img_yml[img_name]['compatible']:
        board_json_file = os.path.splitext(os.path.join(args.json_tree, board_ref.category, board_ref.resc))[0] + '.json'
        with FileLock(board_json_file + ".lock", timeout=-1):
            with open(board_json_file, 'r') as fp:
                board_json = json.load(fp)
            if distro_name not in board_json['os']:
                # Ensure distro exists
                board_json['os'][distro_name] = []
            if not any(existing_releases['name'] == distro_release['name'] for existing_releases in board_json['os'][distro_name]):
                # Ensure distro release exists
                board_json['os'][distro_name].append(distro_release)
            # Finally append the new imagesuite
            next(matching_release for matching_release in board_json['os'][distro_name] if matching_release['name'] == distro_release['name'])['imagesuites'].append(img_json)

            with open(board_json_file, 'w') as fp:
                json.dump(board_json, fp, indent=2)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input_file", action='store',
                            help="YAML document to be parsed",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-j", "--json_tree", action='store',
                            help="Search path for JSONs to be patched",
                            required=False, type=str, default='build'
                            )
    arg_parser.add_argument("-s", "--search_path", action='store',
                            help="Search path for YAMLs being referenced",
                            required=False, type=str, default=''
                            )
    main(arg_parser.parse_args())
