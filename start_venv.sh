#!/bin/bash

VENV_DIR=node_env
if [ -d "$VENV_DIR" ]; then
  echo "VENV FOUND"
  source "$VENV_DIR/bin/activate"
else

  case "$(uname -s)" in

   Darwin)
      echo 'Mac OS X'
      python3 -m venv $VENV_DIR
     ;;

   Linux)
      echo 'Linux'
      sudo apt-get install python3-venv
      python3 -m venv $VENV_DIR
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
      echo 'Other OS'
     ;;
  esac

  source "$VENV_DIR/bin/activate"
  pip install -r startup_requirements.txt

fi
python ZeuZ_Node_Installer.py