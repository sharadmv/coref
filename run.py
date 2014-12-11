#!/usr/bin/env python
import sys
import argparse

import coref

def start(args):
    coref.listen(args.port, host='0.0.0.0')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('command')
    argparser.add_argument('-p', '--port', type=int, default=8080)

    args = argparser.parse_args()
    if args.command not in locals():
        print "Unable to find command: %s" % args.command
        sys.exit(1)
    locals()[args.command](args)
