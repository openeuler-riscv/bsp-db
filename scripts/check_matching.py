#!/usr/bin/env python3

import argparse
import yaml
import json
import sys
import os
from collections.abc import Hashable, Sequence, Mapping, Set
import datetime

import yml_helper


class YMLStructCompare:
    def __init__(self, yml_a, yml_b):
        self.yml_a = yml_a
        self.yml_b = yml_b
        self.history = []

    def compare(self):
        self.detect_node_type(self.yml_a, self.yml_b)

    def detect_node_type(self, yml_a, yml_b):
        if isinstance(yml_a, int) or \
            isinstance(yml_a, str) or \
            isinstance(yml_a, float) or \
            isinstance(yml_a, bool) or \
            isinstance(yml_a, datetime.date):
            pass
        elif type(yml_a) != type(yml_b):
            raise Exception("Type mismatch: A=%s B=%s @ %s"%(str(type(yml_a)), str(type(yml_b)), str(self.history)))
        elif isinstance(yml_a, Mapping):
            self.compare_mapping(yml_a, yml_b)
        elif isinstance(yml_a, Sequence):
            self.compare_sequence(yml_a, yml_b)
        elif isinstance(yml_a, Set):
            self.compare_set(yml_a, yml_b)
        elif isinstance(yml_a, yml_helper.FileReference):
            self.compare_fref(yml_a, yml_b)
        else:
            raise Exception("Unsupported type %s @ %s"%(str(type(yml_a)), str(self.history)))

    def compare_mapping(self, yml_a, yml_b):
        if len(yml_a.keys()) != len(yml_b.keys()):
            raise Exception("mappping @ %s has different number of keys"%(str(self.history)))
        for key in yml_a.keys():
            self.history.append(key)
            if key in yml_b:
                self.detect_node_type(yml_a[key], yml_b[key])
            else:
                raise Exception("key %s does not exist"%(str(self.history)))
            self.history.pop()

    def compare_sequence(self, yml_a, yml_b):
        if len(yml_a) != len(yml_b):
            raise Exception("sequence @ %s has different number of items"%(str(self.history)))
        for i in range(0, len(yml_a)):
            self.history.append("[%d]"%(i))
            self.detect_node_type(yml_a[i], yml_b[i])
            self.history.pop()

    def compare_set(self, yml_a, yml_b):
        if len(yml_a) != len(yml_b):
            raise Exception("set size not equal @ %s"%(str(self.history)))

    def compare_fref(self, yml_a, yml_b):
        pass


def main(args: argparse.Namespace):
    yml_a = yml_helper.load_yaml_file(args.input_file[0], base_path=args.root)
    yml_b = yml_helper.load_yaml_file(args.input_file[1], base_path=args.root)
    YMLStructCompare(yml_a, yml_b).compare()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-r", "--root", action='store',
                            help="Root directory for path lookup",
                            default=".", type=str,
                            )
    arg_parser.add_argument("input_file", action='store',
                            help="YAML documents to be compared, resolved based on --root",
                            nargs=2, type=str
                            )
    main(arg_parser.parse_args())
