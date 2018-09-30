#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g
#Inclusão de bibliotecas
CXXLIBS = -lcryptopp

#Geração dos objetos com função main
blockchain: blockchain.o block.o
	$(CXX) $(CXXFLAGS) -o blockchain blockchain.o block.o $(CXXLIBS)

#Criação dos arquivos compilados das libs abaixo
block.o: block.cpp block.h
	$(CXX) $(CXXFLAGS) -c block.cpp $(CXXLIBS)
blockchain.o: blockchain.cpp blockchain.h
	$(CXX) $(CXXFLAGS) -c blockchain.cpp $(CXXLIBS)

#Compilação de tudo
all: blockchain;

#Remoção dos arquivos gerados
clean:
	rm -f blockchain *.o
