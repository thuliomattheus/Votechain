#! /bin/bash
clear
source /home/thulio_sousa/Documentos/TCC/tccVEnv/bin/activate
cd ~/Documentos/TCC/blockchainClient
python manage.py runserver 0.0.0.0:8001

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
