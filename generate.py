#! /usr/bin/env python3


import glob


def main():
    for fname in glob.glob("pages/**/*.html"):
        print(fname)


if __name__ == "__main__":
    main()
