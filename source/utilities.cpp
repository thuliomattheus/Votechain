#include "../headers/utilities.h"

namespace Utilities{

	string StringUtil::applySha256(string s){

		string hashed_s;

		SHA256 hash;

		StringSource ssource(s, true,
				new HashFilter(hash,
					new HexEncoder(
						new StringSink(hashed_s))));

		return hashed_s;

	}

	string StringUtil::pubKeyAsString(RSA::PublicKey pubK){

		string pbK;

		// Aponta o codificador de base64 para atuar sobre a string
		Base64Encoder pubKeySink(new StringSink(pbK));

		// Copia as chaves para as respectivas strings
		pubK.DEREncode(pubKeySink);

		// Necessário para finalizar a escrita das chaves
		pubKeySink.MessageEnd();

		return pbK;

	}

	string StringUtil::privKeyAsString(RSA::PrivateKey privK){

		string pvK;

		// Aponta o codificador de base64 para atuar sobre a string
		Base64Encoder privKeySink(new StringSink(pvK));

		// Copia as chaves para as respectivas strings
		privK.DEREncode(privKeySink);

		// Necessário para finalizar a escrita das chaves
		privKeySink.MessageEnd();

		return pvK;

	}

	SecByteBlock StringUtil::signMessage(RSA::PrivateKey privK, string message){

		// Gerador de número aleatório
		AutoSeededRandomPool rng;

		// Objeto que fará a assinatura utilizando a chave privada do remetente
		RSASS<PSS, SHA256>::Signer signer(privK);

		// Tamanho que será utilizado na assinatura
		// Inicialmente será usado o maior valor possível da classe Signer
		size_t length = signer.MaxSignatureLength();

		// Sequência de bytes que guardará a assinatura
		SecByteBlock signature(length);

		// Assinatura da mensagem 
		length = signer.SignMessage(rng, (const byte*) message.c_str(),
			message.length(), signature);

		// Altere o tamanho da assinatura para o tamanho real da mesma
		signature.resize(length);

		return signature;
	}

	bool StringUtil::verifyMessage(RSA::PublicKey pubK, string message, SecByteBlock signature){

		// Objeto que verificará a assinatura utilizando a chave pública do remetente
		RSASS<PSS, SHA256>::Verifier verifier(pubK);

		// Verificação da mensagem
		bool result = verifier.VerifyMessage((const byte*)message.c_str(),
			message.length(), signature, signature.size());

		return result;
	}

	string StringUtil::documentToString(const Document& d){

		StringBuffer buffer;
		Writer<StringBuffer> writer(buffer);
		d.Accept(writer);

		return buffer.GetString();

	}

	Document StringUtil::stringToDocument(string s){

		Document d;
		d.Parse(s.c_str());

		return d;

	}

	Document StringUtil::fileToDoc(string filePath){
		FILE* f = fopen(filePath.c_str(), "r");
		Document d;
		char readBuffer[65536];
		FileReadStream frs(f, readBuffer, sizeof(readBuffer));
		d.ParseStream(frs);
		fclose(f);

		return d;
	}

}
