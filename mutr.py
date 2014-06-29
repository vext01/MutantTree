#!/usr/bin/env python3
import os, sys

class MutantTreeError(Exception): pass

def path_to_elems(path):
    return path.split(os.path.sep)

def do_rename(old, new):
    if old == new: return
    print("RENAME: %s -> %s" % (old, new))
    os.rename(old, new)

class PathFile():
    def __init__(self, name):
        self.old_name = name
        self.new_name = name

    def rename(self, cur_path):
        #full_name = os.path.join(cur_path, self.old_name)
        # XXX for now hardcoded lowercasing, use regex eventually.
        old_name =  os.path.join(cur_path, self.old_name)
        new_name = os.path.join(cur_path, self.old_name.lower())
        do_rename(old_name, new_name)

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

        # Sort the children by directories first. This ensures that leaf nodes
        # are renamed first.
        children.sort(key=lambda x : 1 if type(x) == PathDir else 2)

        dir_name = path_to_elems(path)[-1]
        return cls(dir_name, children)

    def rename(self, cur_path):
        here_path = os.path.join(cur_path, self.old_name)
        for c in self.children:
            c.rename(here_path) # rename all children first. important!

        # XXX
        do_rename(here_path, os.path.join(cur_path, self.old_name.lower()))

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
    #path_minus_last = os.path.abspath(os.path.join(path, ".."))
    tree.rename(os.path.abspath(path))

if __name__ == "__main__":
    entry_point()
