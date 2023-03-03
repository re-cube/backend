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

api_doc:
	uvicorn app:app --host 0.0.0.0 --port 8000 &
	sleep 3
	mkdir -p docs
	curl http://localhost:8000/openapi.json | ./scripts/json2yaml.py > docs/openapi.yaml
	pkill -f 'uvicorn app:app'
