#!/usr/bin/env python3

import argparse
import yaml
import json
import os




def main(args: argparse.Namespace):
    with open(args.input, "r") as f:
        yml = yaml.load(f.read(), yaml.SafeLoader)
    result = {}
    result["extension"] = []
    for src_ext in yml["extension"]:
        result["extension"].append(src_ext[0])
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input", action='store',
                            help="input yaml file",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-o", "--output", action='store',
                            help="output json file",
                            required=True, type=str,
                            )
    main(arg_parser.parse_args())
