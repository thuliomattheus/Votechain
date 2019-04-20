#! /bin/bash
#####################################
# Para chamar corretamente, digite: #
#         . ativarVEnv.sh           #
#               ou                  #
#       source ativarVEnv.sh        #
#####################################

# Limpa o console
clear
# Ativa a virtualenv
source /home/thulio_sousa/Documentos/TCC/tccVEnv/bin/activate
# Instala as dependências do projeto
pip install -r /home/thulio_sousa/Documentos/TCC/requirements.txt
