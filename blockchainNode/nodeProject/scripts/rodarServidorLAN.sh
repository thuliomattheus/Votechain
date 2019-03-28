#! /bin/bash
clear
source /home/thulio_sousa/Documentos/tccVEnv/bin/activate
cd ~/Documentos/tccVEnv/TCC/blockchainNode
python manage.py runserver 0.0.0.0:8000

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
