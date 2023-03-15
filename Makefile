ifneq (,$(wildcard ./.env))
	include .env
	export
endif

CODE = src
CODE_TESTS = test
PROJECT_NAME = image_to_code
TEST = pytest $(CODE_TESTS) --verbosity==2 --showlocals --strict-markers --log-level=DEBUG --code_type=python
TEST_COV = pytest $(CODE_TESTS) --cov --verbosity==2 --showlocals --strict-markers --log-level=DEBUG --cov-fail-under=10 --code_type=python


test:
	export PYTHONPATH=src && &(TEST)

test-cov:
	export PYTHONPATH=src && &(TEST_COV)

lint:
	export PYTHONPATH=src && pylint --jobs 1 --rcfile=setup.cfg $(CODE)

clean:
	find . -name 'pycache' -type d | xargs rm -fr
	find . -name '.coverage' -delete
	find . -name '.ipynb_checkpoints' -type d | xargs rm -fr
	find . -name '.pytest_cache' -type d | xargs rm -fr
