import socket
import ssl
import sys
from datetime import datetime
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_domains(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file]

def ssl_validation(domain):
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_OPTIONAL
    
    port = 443
    try:
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain) as sock:
            sock.settimeout(4)
            sock.connect((domain, port))
            cert = sock.getpeercert()

            # Validação de data de expiração
            notafter = cert.get('notAfter')
            if notafter:
                exp_date = datetime.strptime(notafter, '%b %d %H:%M:%S %Y %Z')
            else:
                exp_date = 'Data de expiração não disponível'

            # Emissor do Certificado
            issuer_common_name = None
            issuer_organization_name = None
            for issuer_field in cert.get('issuer', []):
                for key, value in issuer_field:
                    if key == 'commonName':
                        issuer_common_name = value
                    elif key == 'organizationName':
                        issuer_organization_name = value

            logging.info(f'Testando domínio: {domain} | Data de expiração: {exp_date} | '
                         f'Emissor: {issuer_common_name}, {issuer_organization_name}')
            
    except ssl.SSLError as e:
        logging.error(f'Erro SSL ao tentar conectar a {domain}: {e}')
    except socket.timeout:
        logging.error(f'Tempo esgotado ao tentar conectar a {domain}')
    except socket.gaierror:
        logging.error(f'Erro de endereço ao tentar conectar a {domain}')
    except Exception as e:
        logging.error(f'Erro ao tentar conectar a {domain}: {e}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Uso: python script.py <caminho_para_o_arquivo_de_dominios>")
        sys.exit(1)
    
    list_domain = sys.argv[1]
    domains = read_domains(list_domain)
    
    for domain in domains:
        ssl_validation(domain)