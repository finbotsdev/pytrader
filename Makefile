
deps:
	brew bundle
	pip install -r requirements.txt

dev:
	export FLASK_APP=app; flask run