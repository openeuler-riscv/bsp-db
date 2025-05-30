import yaml
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import SafeConstructor, ConstructorError
from yaml.resolver import Resolver
from yaml.nodes import MappingNode, SequenceNode, ScalarNode
import collections
import os


class MergeNode:
    pass

class SafeIncConstructor(SafeConstructor):
    def construct_include_nodes(self, node):
        target_file = None
        target_node = []
        if isinstance(node, MappingNode):
            for key_node, value_node in node.value:
                if key_node.tag == "tag:yaml.org,2002:str" and key_node.value == "path" and value_node.tag == "tag:yaml.org,2002:str":
                    target_file = value_node.value
                    continue
                if isinstance(value_node, SequenceNode):
                    for value_node_value in value_node.value:
                        if value_node_value.tag == "tag:yaml.org,2002:str":
                            target_node.append(value_node_value.value)
                        else:
                            raise ConstructorError(None, None,
                                "expected a str node, but found %s" % target_node.id,
                                target_node.start_mark)
                    continue
            if not target_file:
                raise ConstructorError(None, None,
                        "path not provided for node %s" % item_node.id,
                        item_node.start_mark)
        elif isinstance(node, ScalarNode):
            target_file = node.value
        else:
            raise ConstructorError(None, None,
                    "expected a mapping node or a scalar node, but found %s" % node.id,
                    node.start_mark)

        try:
            norm_filename = self.parse_file_path(target_file)
        except Exception as e:
            current_file = os.path.normpath(self.base_path + self.inc_stack[len(self.inc_stack) - 1])
            raise Exception("While processing inclusion \"%s\" from \"%s\""%(target_file, current_file))
        self.inc_stack.append(norm_filename)
        with open(self.base_path + norm_filename) as f:
            nested_data = yaml.compose(f, SafeIncLoader)
            # Walk through nodes
            # Only mapping nodes are supported by now
            for path_segment in target_node:
                if isinstance(nested_data, MappingNode):
                    found = False
                    for key_node, value_node in nested_data.value:
                        if key_node.tag == "tag:yaml.org,2002:str" and key_node.value == path_segment:
                            found = True
                            nested_data = value_node
                            break
                    if not found:
                        raise Exception("invalid node")
                else:
                    raise ConstructorError(None, None,
                            "expected a mapping node, but found %s" % nested_data.id,
                            nested_data.start_mark)
        return nested_data

    def construct_include(self, node, deep=False):
        included_nodes = self.construct_include_nodes(node)
        data = self.construct_object(included_nodes, True)
        yield data

    def construct_merge(self, node, deep=False):
        # Mark the merging condition
        yield MergeNode()

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            values = []
            if isinstance(key, MergeNode):
                # Merging
                if isinstance(value_node, SequenceNode):
                    value_list = self.construct_object(value_node, deep=deep)
                    for value in reversed(value_list):
                        values.append(value)
                elif isinstance(value_node, MappingNode):
                    value = self.construct_object(value_node, deep=deep)
                    values.append(value)
            elif isinstance(key, collections.abc.Hashable):
                map_value = self.construct_object(value_node, deep=deep)
                values.append({key: map_value})
            else:
                raise ConstructorError("while constructing a mapping", node.start_mark,
                        "found unexpected key", key_node.start_mark)

            for value in values:
                if isinstance(value, dict):
                    mapping.update(value)
                elif isinstance(value, set):
                    mapping.update({key: None for key in value})

        return mapping

SafeIncConstructor.add_constructor(u'!inc', SafeIncConstructor.construct_include)
SafeIncConstructor.add_constructor(u'tag:yaml.org,2002:merge', SafeIncConstructor.construct_merge)

class SafeIncLoader(Reader, Scanner, Parser, Composer, SafeIncConstructor,
                    Resolver):

    def __init__(self, stream, base_path="."):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeIncConstructor.__init__(self)
        Resolver.__init__(self)

        self.base_path = base_path
        self.inc_stack = []

    def parse_file_path(self, filename):
        # If the filename is an absolute path:
        #   It will be resolved with self.base_path as root
        # If the filename is a relative path:
        #   It will be resolved based on the directory of current file being processed
        # Additionally:
        #   filename must resides under self.base_path:
        #     filename is abs:
        #       filename is resolved always under base_path
        #     filename is rel:
        #       filename is reconstructed relative to current file, and not exceeding base_path
        if os.path.isabs(filename):
            return os.path.normpath(filename)
        else:
            curr_file_dir = os.path.dirname(self.inc_stack[len(self.inc_stack) - 1])
            if os.path.normpath("/rootguard" + curr_file_dir + os.path.sep + filename) != os.path.normpath("/rootguard" + os.path.normpath(curr_file_dir + os.path.sep + filename)):
                raise Exception("Relative path exceeding base_path")
            else:
                return os.path.normpath(curr_file_dir + os.path.sep + filename)


    @classmethod
    def load_file(cls, filename, base_path="."):
        # Use "absolute" path as stack records
        if not filename.startswith(os.path.sep):
            filename = os.path.sep + filename
        # Always resolve filename based on base_path
        with open(os.path.normpath(base_path + filename)) as f:
            loader = cls(f, base_path=base_path)
            loader.inc_stack.append(filename)
            try:
                data = loader.get_single_data()
            finally:
                loader.dispose()
        return data


class FileReference():
    def __init__(self, path):
        self.path = path

    @classmethod
    def constructor(cls, loader, node):
        return cls(loader.parse_file_path(loader.construct_scalar(node)))


def load_yaml_file(filename: str, base_path="."):
    SafeIncConstructor.add_constructor(u'!fref', FileReference.constructor)

    return SafeIncLoader.load_file(filename, base_path=base_path)
