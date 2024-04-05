import sys


def debug(*args: object):
    for i in args:
        print(i, file=sys.stderr, end=" ")
    print(file=sys.stderr)
    with open("open.log", "a") as f:
        for i in args:
            print(i, file=f, end=" ")
        print(file=f)
