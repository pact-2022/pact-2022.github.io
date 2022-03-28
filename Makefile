all: img output/pact22-template.zip
	mkdir -p output
	python3 generate.py cfp.md > output/cfp-pact-2022.txt
	set -e; for pg in pages/*.html; do \
		python3 generate.py $${pg} > output/$${pg##pages/} ; \
	done
	cp -Rv static/* output/

output/pact22-template.zip: ./submission-template/pact22/pact22-template.tex
	mkdir -p output
	cd submission-template && zip ../$@ $$(git ls-files)

img: \
	static/images-generated/chicago-skyline-800px.jpeg \
	static/images-generated/illinois-wordmark.png \
	static/images-generated/ieee-tcpp-logo-300px.png

static/images-generated/chicago-skyline-800px.jpeg: image-src/pedro-lastra-Nyvq2juw4_o-unsplash.jpg
	mkdir -p "./$(dir $@)"
	gm convert -geometry 800x800 $< $@

static/images-generated/illinois-wordmark.png: image-src/illinois-wordmark-dark-letters.pdf
	mkdir -p "./$(dir $@)"
	gm convert -density 1000 -geometry 300x300 $< $@

static/images-generated/ieee-tcpp-logo-300px.png: image-src/ieee-tcpp-logo.png
	mkdir -p "./$(dir $@)"
	gm convert -geometry 300x300 $< $@

clean:
	rm -Rf static/images-generated output

publish: all
	./publish.sh

.PHONY: all
