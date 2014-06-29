#!/usr/bin/env python3
import os, sys

class MutantTreeError(Exception): pass

def path_to_elems(path):
    return path.split(os.path.sep)

class PathFile():
    def __init__(self, name):
        self.old_name = name
        self.new_name = name

    def __str__(self):
        return "%s:%s" % (self.old_name, self.new_name)

class PathDir(PathFile):
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    @classmethod
    def make(cls, path):
        files_here = os.listdir(path)
        children = []

        for fl in files_here:
            full_path = os.path.join(path, fl)
            if os.path.isdir(full_path):
                children.append(PathDir.make(full_path))
            elif os.path.isfile(full_path):
                children.append(PathFile(fl))

        dir_name = path_to_elems(path)[-1]
        return cls(dir_name, children)

    def __str__(self):
        """ Print a tree, just for debugging really. """
        return "%s:%s[%s]" % (
                self.old_name,
                self.new_name,
                ", ".join([ str(x) for x in self.children ])
                )

def entry_point():
    try:
        path = sys.argv[1]
    except IndexError:
        path = "."

    tree = PathDir.make(path)
    print(tree)

if __name__ == "__main__":
    entry_point()
