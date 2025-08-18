#!/usr/bin/env python3
import argparse
import os
import json
import re


def main(args: argparse.Namespace):
    boardlist = []
    id_regex = re.compile(r".*products\/(.+)\/(.+)\.json$")

    for board_json_file in args.input_files:
        with open(board_json_file, 'r') as fp:
            board_json = json.load(fp)

        vendor_id, board_id = id_regex.match(board_json_file).groups()

        curr_board = {}
        curr_board["name"] = board_json["name"]
        curr_board["id"] = board_id
        curr_board["vendor"] = {
            "name": board_json["vendor"]["name"],
            "id": vendor_id
        }
        curr_board["soc"] = {
            "name": board_json["soc"]["name"],
            "vendor": board_json["soc"]["vendor"]["name"],
        }
        curr_board["thumbnail"] = board_json["pictures"][0] if len(board_json["pictures"]) > 0 else None
        curr_board["mark"] = []

        for distro in board_json["imagesuites"]:
            for distro_release in distro["releases"]:
                for suite in distro_release["imagesuites"]:
                    if suite["kernel"]["type"] in [ "RVCK", "OLK" ]:
                        curr_board["mark"] = list(set(curr_board["mark"] + [suite["kernel"]["type"]]))
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
                            help="Root of dist dir",
                            required=True, type=str
                            )
    arg_parser.add_argument("input_files", action='store',
                            help="JSON documents to be combined",
                            nargs='+', type=str
                            )
    main(arg_parser.parse_args())
