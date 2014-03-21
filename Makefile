serve:
	python -m SimpleHTTPServer

push:
	git push
	-git branch -D gh-pages
	git checkout -b gh-pages
	git push -f -u origin gh-pages
	git checkout master

update:
	python dl.py
	python prep.py

lint:
	jshint bracket.js

.PHONY: serve push update lint
