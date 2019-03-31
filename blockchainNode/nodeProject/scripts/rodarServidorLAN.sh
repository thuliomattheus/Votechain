#! /bin/bash
clear
source /home/thulio_sousa/Documentos/TCC/tccVEnv/bin/activate
cd ~/Documentos/TCC/blockchainNode
python manage.py runserver 0.0.0.0:8000

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
