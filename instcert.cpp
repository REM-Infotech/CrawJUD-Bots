#include <Python.h>
#include <windows.h>
#include <wincrypt.h>
#include <iostream>
#include <string>

#pragma comment(lib, "Crypt32.lib")

bool InstallCertificate(const std::string& certPath) {
    // Abra o arquivo de certificado
    HANDLE hFile = CreateFileA(certPath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        std::cerr << "Erro ao abrir o arquivo de certificado." << std::endl;
        return false;
    }

    // Obtenha o tamanho do certificado
    DWORD fileSize = GetFileSize(hFile, NULL);
    if (fileSize == INVALID_FILE_SIZE) {
        std::cerr << "Erro ao obter o tamanho do arquivo." << std::endl;
        CloseHandle(hFile);
        return false;
    }

    // Leia o conteúdo do certificado no buffer
    BYTE* certBuffer = new BYTE[fileSize];
    DWORD bytesRead = 0;
    if (!ReadFile(hFile, certBuffer, fileSize, &bytesRead, NULL)) {
        std::cerr << "Erro ao ler o arquivo de certificado." << std::endl;
        delete[] certBuffer;
        CloseHandle(hFile);
        return false;
    }

    CloseHandle(hFile);

    // Converta o buffer de bytes para um certificado
    PCCERT_CONTEXT pCertContext = CertCreateCertificateContext(X509_ASN_ENCODING | PKCS_7_ASN_ENCODING, certBuffer, fileSize);
    delete[] certBuffer;

    if (!pCertContext) {
        std::cerr << "Erro ao criar contexto do certificado." << std::endl;
        return false;
    }

    // Abra o armazenamento de certificados pessoal do usuário
    HCERTSTORE hCertStore = CertOpenStore(CERT_STORE_PROV_SYSTEM, 0, NULL, CERT_SYSTEM_STORE_CURRENT_USER, L"MY");
    if (!hCertStore) {
        std::cerr << "Erro ao abrir o armazenamento de certificados." << std::endl;
        CertFreeCertificateContext(pCertContext);
        return false;
    }

    // Adicione o certificado ao armazenamento
    if (!CertAddCertificateContextToStore(hCertStore, pCertContext, CERT_STORE_ADD_REPLACE_EXISTING, NULL)) {
        std::cerr << "Erro ao adicionar o certificado ao armazenamento." << std::endl;
        CertCloseStore(hCertStore, 0);
        CertFreeCertificateContext(pCertContext);
        return false;
    }

    // Feche o armazenamento e libere o contexto
    CertCloseStore(hCertStore, 0);
    CertFreeCertificateContext(pCertContext);

    std::cout << "Certificado instalado com sucesso!" << std::endl;
    return true;
}

// Função para expor o módulo para Python
PYBIND11_MODULE(cert_installer, m) {
    m.def("install_certificate", &InstallCertificate, "Função para instalar um certificado a partir de um arquivo.");
}
