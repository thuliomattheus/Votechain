#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g # Para mostrar as dependências: -H
#Inclusão de bibliotecas
#CXXLIBS = -lcryptopp

#Geração do executável -arquivo com função main- a partir das libs e objetos necessários
run: wallet.o transaction.o utilities.o block.o blockchain.o
	$(CXX) $(CXXFLAGS) -o run wallet.o transaction.o utilities.o block.o blockchain.o lib/cryptopp/libcryptopp.a

#Criação dos objetos necessários utilizandos as api's e implementações dos mesmos
blockchain.o: source/blockchain.cpp headers/blockchain.h
	$(CXX) $(CXXFLAGS) -c source/blockchain.cpp

block.o: source/block.cpp headers/block.h
	$(CXX) $(CXXFLAGS) -c source/block.cpp

transaction.o: source/transaction.cpp headers/transaction.h
	$(CXX) $(CXXFLAGS) -c source/transaction.cpp

wallet.o: source/wallet.cpp headers/wallet.h
	$(CXX) $(CXXFLAGS) -c source/wallet.cpp

utilities.o: source/utilities.cpp headers/utilities.h
	$(CXX) $(CXXFLAGS) -c source/utilities.cpp

#Compilação de tudo
all: run;

#Remoção dos arquivos gerados
clean:
	rm -f run *.o
