from __future__ import print_function
import os
import sys
import argparse
from .parser import ECfg


def main():
    parser = argparse.ArgumentParser(description='Parse e.cfg files')
    parser.add_argument('filename')
    parser.add_argument('--output',
                        help='Output format',
                        choices=('text', 'xml', 'json'),
                        default='text')
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print('Input file not found' % args.filename)
        sys.exit(1)

    with open(args.filename) as f:
        text = f.read()

    result = ECfg(text)

    if args.output == 'text':
        print(result.text())
    elif args.output == 'xml':
        print(result.xml())
    elif args.output == 'json':
        print(result.json(indent=2))
    else:
        print('Unknown output format')
        sys.exit(1)


if __name__ == '__main__':
    main()
