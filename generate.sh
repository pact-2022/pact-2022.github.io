#! /bin/bash

gm convert -geometry 800x800 \
        image-src/pedro-lastra-Nyvq2juw4_o-unsplash.jpg \
        static/images-generated/chicago-skyline-800px.jpeg

python3 generate.py
