deps:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

prepare: reformat lint

reformat:
	black .
	isort .

check: lint
	black --check .
	isort --check-only .

lint:
	flake8
	pyright .
