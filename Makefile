all: img
	python3 generate.py

img: \
	static/images-generated/chicago-skyline-800px.jpeg \
	static/images-generated/illinois-wordmark.png

static/images-generated/chicago-skyline-800px.jpeg: image-src/pedro-lastra-Nyvq2juw4_o-unsplash.jpg
	mkdir -p "./$(dir $@)"
	gm convert -geometry 800x800 $< $@

static/images-generated/illinois-wordmark.png: image-src/illinois-wordmark-dark-letters.pdf
	mkdir -p "./$(dir $@)"
	gm convert -geometry 300x300 $< $@

clean:
	rm -Rf static/images-generated output
