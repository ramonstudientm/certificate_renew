from datetime import datetime
import pandas as pd
import logging, sys, ssl, socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Certificate:
    def __init__(self, commonName, altName, expDate, creationDate):
        self.commonName = commonName
        self.altName = altName
        self.expDate = expDate
        self.creationDate = creationDate
    
    #def __str__(self):
    #    return f"Common Name: {self.commonName}, Alt Name: {self.altName}, Exp Date: {self.expDate}, Creation Date: {self.creationDate}"
    def to_dict(self):
        return { 'Common Name': self.commonName, 'Alternative Names': ', '.join(self.altName) if self.altName else 'None', 'Expiration Date': self.expDate, 'Creation Date': self.creationDate }

def get_domains_list(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file]

def get_certificate_info(domain):
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    try:
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain) as sock:
            sock.settimeout(4)
            sock.connect((domain, 443))
            cert = sock.getpeercert()

            common_name = dict(x[0] for x in cert['subject'])['commonName']
            altName = [x[1] for x in cert.get('subjectAltName', [])]
            not_after = cert['notAfter']
            expDate = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            not_before = cert['notBefore']
            creationDate = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
            return Certificate(common_name, altName, expDate, creationDate)
        
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
        logging.error("Uso: python script.py domain.list ")
        sys.exit(1)
    
list_domain = sys.argv[1]
domains = get_domains_list(list_domain)
    
    

csv_name = 'default.csv'
try:
    if len(sys.argv) >= 2:
        csv_name = sys.argv[2]
except:
    pass     
        
certificates = []
for domain in domains:
    cert_info = get_certificate_info(domain) 
    if cert_info:
        logging.info(cert_info)
        print(cert_info)
        certificates.append(cert_info.to_dict())
        df = pd.DataFrame(certificates)
        df.to_csv(csv_name, index=False)
        logging.info(f"Informações dos certificados exportadas para '{csv_name}'")

