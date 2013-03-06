#!/bin/bash

set -e

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo "$TEST failed"
    exit $EXIT_STATUS
  else
    echo "$TEST passed"
  fi
}

VIRTUALENV_DIR=/var/tmp/virtualenvs/$(echo ${JOB_NAME} | tr ' ' '-')
export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

virtualenv --clear --no-site-packages $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt
pip install -r requirements_for_tests.txt

nosetests -v
display_result $? 1 "Unit tests"

behave --no-color
display_result $? 2 "Feature tests"

$(dirname $0)/pep-it.sh
display_result $? 3 "Code style check"