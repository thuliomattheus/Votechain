#! /bin/bash
cd ~/Documentos/TCC/blockchainNode
rm nodeDatabase.sqlite3
rm -r nodeProject/nodeApp/migrations
rm -r nodeProject/voteReusableApp/migrations
python manage.py makemigrations nodeApp voteReusableApp
python manage.py migrate
cd -

