#! /bin/bash
cd ~/Documentos/tccVEnv/TCC/blockchainNode
rm db.sqlite3
rm -r nodeProject/nodeApp/migrations
python manage.py makemigrations nodeApp
python manage.py migrate
cd -

