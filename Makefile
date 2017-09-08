start:
	python app/weber.py

test:
	@echo "running tests"
	@pytest tests/

build:
	python setup.py sdist

set_version:
	@echo VERSION=\"${to}\" > version.py
	@echo Version set to ${to}

version:
	@more version.py

clean:
	rm -rf dist/
