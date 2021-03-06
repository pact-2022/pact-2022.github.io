# Web page for PACT 2022

[PACT](http://pactconf.org) is the International Conference on Parallel
Architectures and Compilation Techniques. This repository contains the source
code for its web page. Any changes here will automatically propage to the
public site, via Github Actions and Github Pages (where the page is hosted).

The page is accessible at https://pact22.cs.illinois.edu/.

## Making simple changes

If you would like to edit the site, very likely what you want is under the
`pages/` subdirectory. You can make simple changes right here on Github
by editing the file. If you're not sure that you're doing it right,
please suggest changes via a pull request rather than directly editing
the `main` branch.

## Making bigger changes

If you are making bigger changes (such as changing how things look), you
may want to build the site locally. To do so, run
```
python3 -m pip install requirements.txt
```
and install [GraphicsMagick](http://www.graphicsmagick.org/) so that it is
available on the path. Once that's done, simply run
```
make
```
and look at the generated site under `output/`.
