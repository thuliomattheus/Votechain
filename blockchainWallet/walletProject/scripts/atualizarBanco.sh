#! /bin/bash
cd ~/Documentos/TCC/blockchainWallet
python manage.py makemigrations walletApp
python manage.py migrate
cd -

