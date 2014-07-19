#!/usr/bin/env python

import sys

if sys.version_info < (2, 7):
    print("This script requires at least Python 2.7.")
    print("Please, update to a newer version: http://www.python.org/download/releases/")
    sys.exit(1)

import os

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR)

import slimit

def main():
    js_root = os.path.join(os.path.dirname(DIR), 'js')
    src = os.path.join(js_root, 'threeio.js')
    dst = os.path.join(js_root, 'threeio.min.js')

    print('Minifying %s > %s' % (src, dst))

    with open(src) as fs:
        data = fs.read()

    minified = slimit.minify(data, mangle=True, mangle_toplevel=False)
    with open(dst, 'w') as fs:
        fs.write(minified)

if __name__ == '__main__':
    main()
