#!/bin/bash
set -e
set -x

# set up wait for mysql container to start up
until nc -z -v -w30 mysql-urlwordcloud 3306
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

echo "DB Connected"

echo "Pytest running (execute pytest)"
pytest

echo "pytest returned"
