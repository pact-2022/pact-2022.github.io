#! /usr/bin/env python3


import glob

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.lexer import Lexer as LexerBase
import os
import shutil
from pathlib import Path
import markdown
import re


# {{{ mako lexer without ## comments (which conflict with markdown)

class Lexer(LexerBase):
    def match_control_line(self):
        # Original version:
        # https://github.com/sqlalchemy/mako/blob/7e52b60b7dac75a3c7177e69244123c0dad9e9d9/mako/lexer.py#L421-L457
        # (comment handling deleted)
        import mako.exceptions as exceptions
        import mako.parsetree as parsetree
        match = self.match(
            r"(?<=^)[\t ]*(%(?!%))[\t ]*((?:(?:\\\r?\n)|[^\r\n])*)"
            r"(?:\r?\n|\Z)",
            re.M,
        )
        if not match:
            return False

        operator = match.group(1)
        text = match.group(2)
        if operator == "%":
            m2 = re.match(r"(end)?(\w+)\s*(.*)", text)
            if not m2:
                raise exceptions.SyntaxException(
                    "Invalid control line: '%s'" % text,
                    **self.exception_kwargs,
                )
            isend, keyword = m2.group(1, 2)
            isend = isend is not None

            if isend:
                if not len(self.control_line):
                    raise exceptions.SyntaxException(
                        "No starting keyword '%s' for '%s'" % (keyword, text),
                        **self.exception_kwargs,
                    )
                elif self.control_line[-1].keyword != keyword:
                    raise exceptions.SyntaxException(
                        "Keyword '%s' doesn't match keyword '%s'"
                        % (text, self.control_line[-1].keyword),
                        **self.exception_kwargs,
                    )
            self.append_node(parsetree.ControlLine, keyword, isend, text)
        else:
            raise AssertionError()

        return True

# }}}


# {{{ remove common indentation

def remove_common_indentation(code: str, require_leading_newline: bool = True):
    r"""Remove leading indentation from one or more lines of code.

    Removes an amount of indentation equal to the indentation level of the first
    nonempty line in *code*.

    :param code: Input string.
    :param require_leading_newline: If *True*, only remove indentation if *code*
        starts with ``\n``.

    :returns: A copy of *code* stripped of leading common indentation.
    """
    if "\n" not in code:
        return code

    if require_leading_newline and not code.startswith("\n"):
        return code

    lines = code.split("\n")
    while lines[0].strip() == "":
        lines.pop(0)
    while lines[-1].strip() == "":
        lines.pop(-1)

    if lines:
        base_indent = 0
        while lines[0][base_indent] in " \t":
            base_indent += 1

        for line in lines[1:]:
            if line[:base_indent].strip():
                raise ValueError("inconsistent indentation")

    return "\n".join(line[base_indent:] for line in lines)

# }}}


def filter_markdown(s):
    return markdown.markdown(remove_common_indentation(s))


OUTPUT_DIR = Path("output")

DATA = {
        "base_dir": ".",
        "conf_name": "PACT 2022",
        "conf_dates": "October 10&ndash;12, 2022",
        "markdown": filter_markdown,
        }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in glob.glob("pages/**/*.html", recursive=True):
        fname = Path(fname)
        with open(fname, "r") as infile:
            tpl = Template(
                    infile.read(),
                    strict_undefined=True,
                    lexer_cls=Lexer,
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

# vim: foldmethod=marker
