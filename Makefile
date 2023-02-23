deps:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

prepare: reformat check

reformat:
	black .
	isort .

check: lint
	pytest -v
	black --check .
	isort --check-only .

lint:
	flake8
	pyright .
