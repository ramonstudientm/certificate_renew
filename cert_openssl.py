# uso de openssl para tentar conectar no host caso a comunicação com socket 1 não funcione
import sys, os
from datetime import datetime

cert_dados = {}
#valida se está com argumento
if len(sys.argv) < 2:
    print(f'usage: python3 cert_openssl.py domains.txt\n')
    exit(0)
else:
        #leitura do arquivo + atribuição da variavel domain
    list_domain = sys.argv[1]
    port = 443
    with open(list_domain) as file:
        domains = file.readlines()
        for domain in domains:
            domain = domain.rstrip('\n')
#/bin/bash -c 'openssl s_client -servername {domain} -connect {domain}:{port}'"
            validate = os.system("openssl s_client -servername {domain} -connect {domain}:{port}")
            print(f'{domain} - {validate}')