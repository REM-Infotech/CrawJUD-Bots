#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>
#include <iostream>

#pragma comment(lib, "crypt32.lib")

bool InstallCertificate(const wchar_t *pfxFilePath, const wchar_t *password)
{
    // Carrega o arquivo PFX
    HCERTSTORE hCertStore = nullptr;
    CRYPT_DATA_BLOB pfxData = {0};
    FILE *pFile = nullptr;

    // Abre o arquivo PFX para leitura
    pFile = _wfopen(pfxFilePath, L"rb");
    if (!pFile)
    {
        wprintf(L"Falha ao abrir o arquivo PFX.\n");
        return false;
    }

    // Obtém o tamanho do arquivo PFX
    fseek(pFile, 0, SEEK_END);
    long fileSize = ftell(pFile);
    fseek(pFile, 0, SEEK_SET);

    // Lê o conteúdo do arquivo PFX
    BYTE *fileBuffer = (BYTE *)malloc(fileSize);
    fread(fileBuffer, 1, fileSize, pFile);
    fclose(pFile);

    // Define o CRYPT_DATA_BLOB para o conteúdo lido
    pfxData.pbData = fileBuffer;
    pfxData.cbData = fileSize;

    // Importa o certificado do arquivo PFX
    if (!PFXIsPFXBlob(&pfxData))
    {
        wprintf(L"Este não é um arquivo PFX válido.\n");
        free(fileBuffer);
        return false;
    }

    HCRYPTPROV hCryptProv = 0;
    CryptAcquireContext(
        &hCryptProv,
        NULL,
        MS_ENHANCED_PROV,
        PROV_RSA_FULL,
        0);

    hCertStore = PFXImportCertStore(&pfxData, password, CRYPT_MACHINE_KEYSET | PKCS12_ALLOW_OVERWRITE_KEY | 0x0010 | CRYPT_MACHINE_KEYSET | CRYPT_EXPORTABLE);

    free(fileBuffer);

    if (!hCertStore)
    {
        wprintf(L"Falha ao importar o certificado.\n");
        return false;
    }
    // Carrega o Store de Certs
    HCERTSTORE StoreCert = CertOpenStore(CERT_STORE_PROV_SYSTEM, 0, 0, CERT_SYSTEM_STORE_CURRENT_USER, L"MY");

    PCCERT_CONTEXT pCertContext = nullptr;
    while ((pCertContext = CertEnumCertificatesInStore(hCertStore, pCertContext)) != nullptr)
    {
        if (!CertAddCertificateContextToStore(StoreCert, pCertContext, CERT_STORE_ADD_REPLACE_EXISTING, nullptr))
        {
            wprintf(L"Falha ao adicionar o certificado ao repositório.\n");
            CertFreeCertificateContext(pCertContext);
            CertCloseStore(hCertStore, 0);
            return false;
        }
    }

    CertFreeCertificateContext(pCertContext);
    CertCloseStore(hCertStore, 0);

    wprintf(L"Certificado instalado com sucesso!\n");
    return true;
}


int main()
{
    const wchar_t *pfxFile = L"\\\\fmv.intranet\\NETLOGON\\CERTIFICADO\\44555059204.pfx";
    const wchar_t *password = L"123456@Pu";

    if (InstallCertificate(pfxFile, password))
    {
        wprintf(L"Instalação concluída.\n");
    }
    else
    {
        wprintf(L"Falha na instalação.\n");
    }

    return 0;
}

// PYBIND11_MODULE(InstallCert, m)
// {

//     m.doc() = "Install cert into Windows Repository"; // optional module docstring

//     m.def("InstallCertificate", &InstallCertificate, "A function that adds two numbers");
// }
