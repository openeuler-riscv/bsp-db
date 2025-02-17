#!/usr/bin/env python3
import argparse
import os
import json


def main(args: argparse.Namespace):
    boardlist = []
    for board_json_file in args.input_files:
        with open(board_json_file, 'r') as fp:
            board_json = json.load(fp)
        curr_board = {
            'name': board_json['name'],
            'vendor': board_json['vendor']['name'],
            'thumbnail': None if len(board_json['pictures']) == 0 else board_json['pictures'][0],
            'soc': {
                'name': board_json['soc']['name'],
                'vendor': board_json['soc']['vendor']['name']
            },
            'isa': [],
            'kernel': [],
            'userspace': [],
            'features': [],
            'uri': os.path.relpath(board_json_file, args.ref_root),
            'status': board_json['status'],
        }
        for dists in board_json['os'].values():
            for os_rels in dists:
                for img in os_rels['imagesuites']:
                    if img['isa']['profile'] not in curr_board['isa']:
                        curr_board['isa'].append(img['isa']['profile'])
                    kernel_identifier = img['kernel']['type'] + '-' + img['kernel']['branch']
                    if kernel_identifier not in curr_board['kernel']:
                        curr_board['kernel'].append(kernel_identifier)
                    if img['userspace'] not in curr_board['userspace']:
                        curr_board['userspace'].append(img['userspace'])
                    for img_feature in img['features']:
                        if img_feature not in curr_board['features']:
                            curr_board['features'].append(img_feature)
        boardlist.append(curr_board)
    with open(args.output_file, 'w') as fp:
        json.dump(boardlist, fp, indent=2)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-o", "--output_file", action='store',
                            help="JSON document to be saved",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-r", "--ref_root", action='store',
                            help="Root of build dir",
                            required=False, type=str, default='build'
                            )
    arg_parser.add_argument("input_files", action='store',
                            help="JSON documents to be combined",
                            nargs='+', type=str
                            )
    main(arg_parser.parse_args())
