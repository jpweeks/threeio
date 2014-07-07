import os
import argparse

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('../../')
addons = os.path.join(os.getcwd(), 'addons')

import sys
sys.path.append(addons)
import threeio
from threeio.exporter import constants


try:
    separator = sys.argv.index('--')
except IndexError:
    print('ERROR: no parameters specified')
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    for key, value in constants.OPTIONS.items():
        if not isinstance(value, bool):
            kwargs = {'type': type(value)}
        else:
            kwargs = {'action':'store_true'}
        kwargs['default'] = value
        parser.add_argument('--%s' % key, **kwargs)

    return vars(parser.parse_args(sys.argv[separator+1:]))


def main():
    args = parse_args()
    if args[constants.SCENE]:
        threeio.exporter.export_scene(args['filepath'], args)
    else:
        threeio.exporter.export_geometry(args['filepath'], args)


if __name__ == '__main__':
    main()
