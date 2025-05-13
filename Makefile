# Makefile for Python Packaging Environment

# Variables
PACKAGE_DIR := .
DIST_DIR := dist
PACKAGE_NAME := $(shell python3 setup.py --name)
PACKAGE_VERSION := $(shell python3 setup.py --version)
DEB_FILE := ../$(PACKAGE_NAME)_$(PACKAGE_VERSION)-1_all.deb

# Default target
all: help

help:
	@echo "Targets:"
	@echo "  build        - Build wheel and sdist"
	@echo "  upload       - Upload to PyPI"
	@echo "  clean        - Clean build artifacts"
	@echo "  deb          - Build Debian package"
	@echo "  validate     - Check manifest and pyproject"

build:
	python3 -m build

upload: check
	twine check $(DIST_DIR)/*

upload: build
	twine upload $(DIST_DIR)/*

clean:
	rm -rf build/ $(DIST_DIR)/ *.egg-info

validate:
	check-manifest
	validate-pyproject

lint:
	lintian $(DEB_FILE)

deb:
	python3 setup.py --command-packages=stdeb.command bdist_deb
	@echo "Built .deb file at $(DEB_FILE)"

.PHONY: all build upload clean deb validate lint help

