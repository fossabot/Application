BROWSER=firefox
BOLD=\033[1m
NORMAL=\033[0m

default: help

clean: clean-pyc clean-test clean-build clean-docs

clean-build:
	rm -rf .eggs
	rm -rf build
	rm -rf dist

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

clean-test:
	rm -rf .cache
	rm -f .coverage
	rm -rf htmlcov
	rm -rf test/data

clean-docs:
	rm -rf docs/build

docs: clean-docs
	cd docs && $(MAKE) html

docs-see: docs
	$(BROWSER) docs/build/html/index.html

install-docs-requirements:
	pip3 install sphinx
	pip3 install sphinx_rtd_theme

install-tests-requirements:
	pip3 install coveralls
	pip3 install pytest pytest-cov

run:
	@echo "Run option isn't created =)"

test: clean-test
	pytest --cov=application

test-docs:
	@echo "Not implemented"
	#python -m doctest *.rst -v
	#python -m doctest docs/*/*.rst -v

test-details: test
	coverage3 html
	$(BROWSER) htmlcov/index.html

help: cabecalho
	@echo ""
	@echo "Commands"
	@echo "    $(BOLD)clean$(NORMAL)"
	@echo "          Clean files"
	@echo "    $(BOLD)docs$(NORMAL)"
	@echo "          Make the docs"
	@echo "    $(BOLD)docs-see$(NORMAL)"
	@echo "          Make the docs and open it in BROWSER"
	@echo "    $(BOLD)install-docs-requirements$(NORMAL)"
	@echo "          Install the docs requirements"
	@echo "    $(BOLD)install-tests-requirements$(NORMAL)"
	@echo "          Install the tests requirements"
	@echo "    $(BOLD)test$(NORMAL)"
	@echo "          Execute the tests"
	@echo "    $(BOLD)test-details$(NORMAL)"
	@echo "          Execute the tests and shows the result in BROWSER"
	@echo "           - BROWSER=firefox"
	@echo "    $(BOLD)help$(NORMAL)"
	@echo "          Show the valid commands"

cabecalho:
	@echo "$(BOLD)                      _ _            _   _"
	@echo "$     /\               | (_)          | | (_)            "
	@echo "$    /  \   _ __  _ __ | |_  ___  __ _| |_ _  ___  _ __  "
	@echo "$   / /\ \ | '_ \| '_ \| | |/ __|/ _\` | __| |/ _ \| '_ \ "
	@echo "$  / ____ \| |_) | |_) | | | (__| (_| | |_| | (_) | | | |"
	@echo "$ /_/    \_\ .__/| .__/|_|_|\___|\__,_|\__|_|\___/|_| |_|"
	@echo "$          | |   | |                                     "
	@echo "$          |_|   |_|                                     "
	@echo "Link$(NORMAL): https://pypi.org/project/PedalPi-Application/"
