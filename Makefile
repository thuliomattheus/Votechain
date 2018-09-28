#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g
#Inclusão de bibliotecas
CXXLIBS = -lcryptopp

#Geração do objeto block
block: block.o
	$(CXX) $(CXXFLAGS) -o block block.o $(CXXLIBS)

#Compilação das libs necessárias
block.o: block.cpp block.h
	$(CXX) $(CXXFLAGS) -c block.cpp $(CXXLIBS)

#Compilação de tudo
all: block;

#Remoção dos arquivos gerados
clean:
	rm -f block block.o
