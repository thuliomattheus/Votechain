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
source ~/Documentos/Votechain/tccVEnv/bin/activate
# Instala as dependências do projeto
pip install -r ~/Documentos/Votechain/requirements.txt
