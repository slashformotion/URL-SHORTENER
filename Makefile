black:
	@black . --exclude=venv

help:
	@echo "	black: format files"

activate:
	. venv/bin/activate

sdb:
	sqlitebrowser URL/db/sqlite/site.db

make db:
	python test.py