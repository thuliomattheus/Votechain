#! /bin/bash
cd ~/Documentos/TCC/blockchainClient
rm clientDatabase.sqlite3
rm -r privateKeys*
rm -r clientProject/clientApp/migrations
python manage.py makemigrations clientApp
python manage.py migrate
cd -

