#! /bin/bash
clear
source /home/thulio_sousa/Documentos/tccVEnv/bin/activate
cd ~/Documentos/tccVEnv/TCC/blockchainWallet
python manage.py runserver 0.0.0.0:8001

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
