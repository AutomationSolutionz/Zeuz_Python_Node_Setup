#!/bin/bash

VENV_DIR=venv
if [ -d "$VENV_DIR" ]; then
  echo "VENV FOUND"
  source "$VENV_DIR/bin/activate"
else
  sudo apt-get install python3-venv
  python3 -m venv $VENV_DIR
  source "$VENV_DIR/bin/activate"
  pip install -r startup_requirements.txt

fi
python ZeuZ_Node_Installer.py