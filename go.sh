#!/bin/bash

MANAGE_SCRIPT_URL="https://raw.githubusercontent.com/dwyl/smart-home-security-system/install/manage.py"

check_for_python() {
  if ! command -v python3 >/dev/null
  then
    echo "Can't find a Python 3 install, which is needed for the setup script."
    exit 1
  else
    echo "Python3 found, continuing..."
  fi

}

install() {
  check_for_python
  echo "Downloading install manager..."
  wget -q -O manage.py $MANAGE_SCRIPT_URL
  chmod +x manage.py
  echo "Running installer..."
  python3 manage.py install
}

install