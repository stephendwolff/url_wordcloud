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

echo "Tornado running (execute run.py)"
python3 run.py --mysqluser=$MYSQL_USER --mysqlpassword=$MYSQL_PASSWORD --mysqlhost=$MYSQL_HOST --mysqldatabase=$MYSQL_DATABASE


echo "run.py returned"
