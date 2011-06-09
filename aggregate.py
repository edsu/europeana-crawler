#!/usr/bin/env python

import os

def metadata_files():
    for dirpath, dirnames, filenames in os.walk('store'):
        for f in filenames:
            if f != "metadata.nt": 
                continue
            yield os.path.join(dirpath, f)

def aggregate():
    for metadata_file in metadata_files():
        for line in open(metadata_file):
            if not line.startswith("<>"):
                line = line.strip()
                print line

if __name__ == "__main__":
    aggregate()
