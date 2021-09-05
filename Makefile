
deps:
	brew bundle
	pip install -r requirements.txt

data:
	python c-sync-assets.py
	python c-sync-reddit-mentions.py
	python c-sync-etfholdings.py
	python c-sync-prices.py

dev:
	@export FLASK_APP=app; flask run
