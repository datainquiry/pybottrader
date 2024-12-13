doc:
	pdoc src/pybottrader --output-dir docs/api

format:
	black .

test:
	pytest tests

lint:
	pylint pybottrader

typing:
	mypy .
