BUILDDIR      = ./~build

.PHONY: clean-pyc clean-build docs

help:
	@echo "fullclean           remove build artifacts"
	@echo "clean               remove Python file artifacts"
	@echo "qa                  check style with flake8"
	@echo "develop             setup development environment"


.setup-git:
	git config branch.autosetuprebase always
	chmod +x hooks/*
	cd .git/hooks && ln -fs ../../hooks/* .

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage pep8.out \
	    coverage.xml flake.out pytest.xml geo.sqlite MANIFEST
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src -name django.mo | xargs rm -f


fullclean: clean
	find . -name *.sqlite -prune | xargs rm -rf
	@rm -fr .tox
	@rm -fr .cache
	@rm -f django_mb_demo
	@rm -fr src/django_mb.egg-info

develop:
	pip install -U pip
	pip install -e .[dev]
	$(MAKE) .setup-git

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

locale:
	cd src/django_mb && ../../manage.py makemessages --all

qa:
	pep8 src/django_mb tests
	flake8 src/django_mb tests
	isort -rc src/django_mb tests --check-only
	check-manifest
	py.test tests/ --cov-report=html --cov-config=tests/.coveragerc --cov django_mb --create-db

docs:
	rm -f docs/django-mb.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/django_mb
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open ${BUILDDIR}/docs/html/index.html

test:
	coverage erase
	tox
	coverage html
