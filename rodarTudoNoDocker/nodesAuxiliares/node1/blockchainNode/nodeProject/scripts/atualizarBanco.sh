#! /bin/bash
cd /app/blockchainNode
rm nodeDatabase.sqlite3
rm -r nodeProject/nodeApp/migrations
python manage.py makemigrations nodeApp
python manage.py migrate
cd -
