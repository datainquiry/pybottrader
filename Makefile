doc:
	pdoc src/pybottrader --output-dir docs

format:
	black .

test:
	pytest tests
