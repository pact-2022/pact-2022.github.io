#! /usr/bin/env python3


import glob

from mako.template import Template
from mako.lookup import TemplateLookup
import os
import shutil
from pathlib import Path

OUTPUT_DIR = Path("output")

DATA = {
        "confname": "PACT 2022",
        }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in glob.glob("pages/**/*.html", recursive=True):
        fname = Path(fname)
        with open(fname, "r") as infile:
            tpl = Template(infile.read(), strict_undefined=True,
                    lookup=TemplateLookup(["template"]))

        rendered = tpl.render(**DATA)
        outname = OUTPUT_DIR / Path(*fname.parts[1:])
        with open(outname, "w") as outf:
            outf.write(rendered)

    for fname in glob.glob("static/**/*", recursive=True):
        fname = Path(fname)
        if not os.path.isfile(fname):
            continue

        outname = OUTPUT_DIR / Path(*fname.parts[1:])
        os.makedirs(os.path.dirname(outname), exist_ok=True)
        shutil.copy2(fname, outname)


if __name__ == "__main__":
    main()
