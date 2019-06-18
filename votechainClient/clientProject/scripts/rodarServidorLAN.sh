#! /bin/bash
clear
source ~/Documentos/Votechain/tccVEnv/bin/activate
cd ~/Documentos/Votechain/votechainClient
python manage.py runserver 0.0.0.0:9000

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
