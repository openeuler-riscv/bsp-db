#!/usr/bin/env python3
import argparse
import os.path
from filelock import FileLock
from yml_helper import load_yaml_file, FileReference
import json
import re
import datetime


def json_serialize(obj):
    if isinstance(obj, (datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def fetch_distro(ref, base_path):
    distro = load_yaml_file(ref.path, base_path=base_path)
    return distro

def fetch_distro_release(ref, base_path):
    distro_release = load_yaml_file(ref.path, base_path=base_path)
    return distro_release

def main(args: argparse.Namespace):
    img_yml = load_yaml_file(args.input_file, base_path=args.root)
    for suite in img_yml:
        distro_release = fetch_distro_release(suite["userspace"], base_path=args.root)
        distro = fetch_distro(distro_release["belongs_to"], base_path=args.root)

        for revision in suite["revisions"]:
            for target in revision["compatible"]:
                target_json_file = re.sub(r"^([^\.]+)\.(?:[^\.]+\.)?yml$", "/\\1.json", target.path)
                with FileLock(args.root + target_json_file + ".lock", timeout=-1):
                    with open(args.output + target_json_file, "r+") as f:
                        suite_json = {}
                        suite_json["name"] = suite["name"]
                        suite_json["kernel"] = {
                            "type": suite["kernel"]["type"],
                            "version": suite["kernel"]["version"],
                        }
                        suite_json["isa"] = {
                            "march": list(suite["isa"]["march"]),
                            "mabi": suite["isa"]["mabi"]
                        }
                        suite_json["loader"] = suite["loader"]
                        suite_json["flavor"] = suite["flavor"]
                        suite_json["revisions"] = []

                        revision_json = {}
                        revision_json["date"] = revision["date"]
                        revision_json["status"] = revision["status"]
                        revision_json["changelog"] = revision["changelog"]
                        revision_json["files"] = []
                        revision_json["docs"] = []
                        if "regression" in revision:
                            revision_json["regression"] = revision["regression"]

                        target_json = json.load(f)
                        if not any(existing_distro["name"] == distro["name"] for existing_distro in target_json["imagesuites"]):
                            target_json["imagesuites"].append({
                                "name": distro["name"],
                                "releases": []
                            })
                        target_distro_json = next((existing_distro for existing_distro in target_json["imagesuites"] if existing_distro['name'] == distro["name"]), None)
                        if not any(existing_distro_release["name"] == distro_release["name"] for existing_distro_release in target_distro_json["releases"]):
                            target_distro_json["releases"].append({
                                "name": distro_release["name"],
                                "imagesuites": []
                            })
                        target_release_json = next((existing_release for existing_release in target_distro_json["releases"] if existing_release['name'] == distro_release["name"]), None)
                        if not any(existing_suite["name"] == suite["name"] for existing_suite in target_release_json["imagesuites"]):
                            target_release_json["imagesuites"].append(suite_json)

                        for imgfile in revision["files"]:
                            if "exclusive" in imgfile:
                                if not any(exclusive_target for exclusive_target in imgfile["exclusive"] if exclusive_target.path == target.path):
                                    continue
                            file_json = {
                                "url": imgfile["url"],
                                "tags": imgfile["tags"],
                                "hash": imgfile["hash"],
                            }
                            revision_json["files"].append(file_json)
                        for docfile in revision["docs"]:
                            if isinstance(docfile, FileReference):
                                revision_json["docs"].append(os.path.normpath(args.prefix + docfile.path))
                            elif isinstance(docfile, dict):
                                if "exclusive" in docfile:
                                    if not any(exclusive_target for exclusive_target in docfile["exclusive"] if exclusive_target.path == target.path):
                                        continue
                                revision_json["docs"].append(os.path.normpath(args.prefix + docfile["file"].path))

                        suite_json["revisions"].append(revision_json)
                        f.seek(0)
                        json.dump(target_json, f, default=json_serialize, indent=2)
    return

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input_file", action='store',
                            help="YAML document to be parsed",
                            required=True, type=str,
                            )
    arg_parser.add_argument("-r", "--root", action='store',
                            help="Root directory for yml path lookup",
                            default=".", type=str,
                            )
    arg_parser.add_argument("-o", "--output", action='store',
                            help="Output directory for json patching",
                            default=".", type=str,
                            )
    arg_parser.add_argument("-p", "--prefix", action='store',
                            help="URL prefix for resources",
                            default=".", type=str,
                            )
    main(arg_parser.parse_args())
