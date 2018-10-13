#Compilador utilizado
CXX = g++
#Todos os avisos (all warnings) e debug
CXXFLAGS = -Wall -g #-H
#Inclusão de bibliotecas
#CXXLIBS = -lcryptopp

#Geração dos objetos com função main passando as libs e os objetos necessários
myArea: electorArea.o vote.o stringUtil.o voteBlock.o urn.o
	$(CXX) $(CXXFLAGS) -o myArea electorArea.o vote.o stringUtil.o voteBlock.o urn.o lib/cryptopp/libcryptopp.a

#Criação dos arquivos compilados das libs abaixo
urn.o: source/urn.cpp headers/urn.h
	$(CXX) $(CXXFLAGS) -c source/urn.cpp

voteBlock.o: source/voteBlock.cpp headers/voteBlock.h
	$(CXX) $(CXXFLAGS) -c source/voteBlock.cpp

vote.o: source/vote.cpp headers/vote.h
	$(CXX) $(CXXFLAGS) -c source/vote.cpp

electorArea.o: source/electorArea.cpp headers/electorArea.h
	$(CXX) $(CXXFLAGS) -c source/electorArea.cpp

stringUtil.o: source/stringUtil.cpp headers/stringUtil.h
	$(CXX) $(CXXFLAGS) -c source/stringUtil.cpp

#Compilação de tudo
all: myArea;

#Remoção dos arquivos gerados
clean:
	rm -f myArea *.o
