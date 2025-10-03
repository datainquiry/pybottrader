format:
	black .

test:
	pytest tests

lint:
	pylint pybottrader

typing:
	mypy .

upload:
	twine upload -r pybottrader dist/*

doc:
	pdoc pybottrader -o docs
