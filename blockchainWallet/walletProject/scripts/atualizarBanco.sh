#! /bin/bash
cd ~/Documentos/tccVEnv/TCC/blockchainWallet
python manage.py makemigrations walletApp
python manage.py migrate
cd -

