
deps:
	@brew bundle
	-@pip install -U git+https://github.com/mariostoev/finviz
	@pip install -r requirements.txt

crontab:
	python c-sync-crontab.py

data:
	python c-sync-assets.py
	python c-sync-reddit-mentions.py
	python c-sync-etfholdings.py
	python c-sync-prices.py

dev:
	@export FLASK_APP=app; flask run
