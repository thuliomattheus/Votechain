#! /bin/bash
clear
source ~/Documentos/Votechain/tccVEnv/bin/activate
cd ~/Documentos/Votechain/votechainNode
python manage.py runserver 0.0.0.0:8000

#python manage.py runserver [::]:8000 --ipv6

# Para chamar corretamente, digite:
#
# . rodarServidorLAN.sh
#
#        ou
#
# source rodarServidorLAN.sh
