all:: clean extract translate compile

clean:
	-rm -rf locale/
	-rm db.sqlite3
	-find . -name "*.pyc" -exec rm -f {} \;

extract: clean
	./manage.py extract
	./manage.py merge -c

translate: extract
	dennis-cmd translate --pipeline=shouty locale/xx/LC_MESSAGES/django.po

compile:
	msgfmt -o locale/xx/LC_MESSAGES/django.mo locale/xx/LC_MESSAGES/django.po

.PHONY: clean compile extract translate
