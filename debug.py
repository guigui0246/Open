import sys
import logging
from os import PathLike


FILE: PathLike = "./open.log"

print_to_stderr = True
logging.basicConfig(filename=FILE)


def debug(*args: object):
    if print_to_stderr:
        for i in args:
            print(i, file=sys.stderr, end=" ")
        print(file=sys.stderr)
    logging.debug(args)
