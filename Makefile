# Variables
SOURCE = shelf_control

# Functions
define clean
	find . -name __pycache__ | xargs rm -rf
endef

# Commands
all: lint format readme

clean:
	$(call clean)

deps:
	pip3 install -U pip
	pip3 install -r requirements.txt

format:
	@echo Formatting source code using black
	black $(SOURCE) scripts
	@echo

lint:
	@echo Searching for unused imports...
	importchecker $(SOURCE) | grep -v __init__ || true
	@echo

readme:
	python -m scripts.generate_readme > README.md