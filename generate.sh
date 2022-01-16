#! /bin/bash

gm convert -geometry 800x800 \
        image-src/pedro-lastra-Nyvq2juw4_o-unsplash.jpg \
        static/images-generated/chicago-skyline-800px.jpeg
gm convert -geometry 300x300 \
        image-src/illinois-wordmark-dark-letters.pdf \
        static/images-generated/illinois-wordmark.png

python3 generate.py
