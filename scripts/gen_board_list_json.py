#!/usr/bin/env python3
import argparse
import os
import json


def main(args: argparse.Namespace):
    boardlist = []
    for board_json_file in args.input_files:
        with open(board_json_file, 'r') as fp:
            board_json = json.load(fp)

        curr_board = {}
        curr_board["name"] = board_json["name"]
        curr_board["vendor"] = board_json["vendor"]["name"]
        curr_board["soc"] = {
            "name": board_json["soc"]["name"],
            "vendor": board_json["soc"]["vendor"]["name"],
        }
        curr_board["thumbnail"] = board_json["pictures"][0] if len(board_json["pictures"]) > 0 else None
        curr_board["mark"] = []
        curr_board["url"] = os.path.relpath(board_json_file, args.ref_root)

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
