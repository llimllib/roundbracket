serve:
	python -m SimpleHTTPServer 4567

push:
	git push
	-git branch -D gh-pages
	git checkout -b gh-pages
	git push -f -u origin gh-pages
	git checkout master

update:
	python dl.py
	python prep.py
	git commit -m "updating data" teams.json natesilver.csv
	make push

lint:
	jshint bracket.js

.PHONY: serve push update lint
