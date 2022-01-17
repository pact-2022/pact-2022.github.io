#! /usr/bin/env python3

from pathlib import Path
import markdown


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
        "submission_deadline": "April 25, 2022",
        "markdown": filter_markdown,
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(
            description="Run PACT-specific Jinja expansion on INFILE, "
            "sending output to stdout.")
    parser.add_argument("infile", metavar="INFILE",
            help="an integer for the accumulator")

    args = parser.parse_args()

    from jinja2 import Environment, FileSystemLoader
    jinja_env = Environment(
            loader=FileSystemLoader([".", "template"]),
            autoescape=False
            )

    jinja_env.filters["markdown"] = filter_markdown

    fname = Path(args.infile)
    with open(fname, "r") as infile:
        tpl = jinja_env.from_string(infile.read())

    basepath = Path(*fname.parts[1:])

    data = DATA | {
            "current_file": str(basepath)
            }

    from html import unescape
    print(unescape(tpl.render(data)))


if __name__ == "__main__":
    main()

# vim: foldmethod=marker
