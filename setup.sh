#!/bin/bash
cd agent/lagent/
pip install -e .
cd ../..
pip install -r requirements.txt
playwright install
playwright install-deps
