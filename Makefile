.PHONY: install test

install:
	pip install wheel
	python setup.py sdist bdist_wheel
	pip install dist/dhcp_packer-0.0.1-py3-none-any.whl

test:
	pytest tests
