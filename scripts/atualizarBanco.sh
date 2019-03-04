#! /bin/bash
cd ~/Documentos/tccVEnv/TCC
python manage.py makemigrations blockchainApp
python manage.py migrate blockchainApp
