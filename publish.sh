#! /bin/bash

set -eo pipefail

PUB_TMPDIR="$(mktemp -d)"
cp -R output/* "$PUB_TMPDIR"

publish()
{
    git init
    git add .
    git commit -m "Add generated site"
    git push -f git@github.com:pact-2022/pact-2022.github.io.git HEAD:gh-pages
}

(cd "$PUB_TMPDIR" && publish)

# vim: shiftwidth=4
