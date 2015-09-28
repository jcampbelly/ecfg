from __future__ import print_function
import os
import sys
import argparse
from .parser import ECfg


def main(argv=None, out=sys.stdout, err=sys.stderr):
    parser = argparse.ArgumentParser(description='Parse e.cfg files')
    parser.add_argument('filename')
    parser.add_argument('--format',
                        help='Output format',
                        choices=('text', 'xml', 'json'),
                        default='text')
    args = parser.parse_args(argv)

    if not os.path.exists(args.filename):
        err.write('Input file not found')
        return 1

    with open(args.filename) as f:
        text = f.read()

    result = ECfg(text)

    if args.format == 'text':
        out.write(result.text())
    elif args.format == 'xml':
        out.write(result.xml())
    elif args.format == 'json':
        out.write(result.json(indent=2))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
