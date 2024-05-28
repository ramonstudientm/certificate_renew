import socket, ssl, sys
from datetime import datetime
cert_dados = {}
#valida se está com argumento
        #leitura do arquivo + atribuição da variavel domain
list_domain = sys.argv[1]
with open(list_domain) as file:
    domains = file.readlines()
    for domain in domains:
        domain = domain.rstrip('\n')    
            
        # função para validar certificado + printar data de expiração.
        def ssl_validation(domain):
                
            context = ssl.create_default_context()
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT, ssl.CERT_OPTIONAL)
            context.load_default_certs()
            conecta = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
            conecta.settimeout(4)
            port = 443
            try:
                res = socket.gethostbyname(domain)
                conecta.connect((domain, port))
                cert = conecta.getpeercert()
                    # Validação de data de expiração
                notafter = cert['notAfter']
                exp_date = datetime.strptime(notafter, '%b %d %H:%M:%S %Y %Z')
                    # Emissor do Certificado 

                issuer_common_name = None
                issuer_organization_name = None
                for issuer_field in cert['issuer']:
                    for key, value in issuer_field:
                        if key == 'commonName':
                            issuer_common_name = value
                        elif key == 'organizationName':
                            issuer_organization_name = value
                            print(f'Testando dominio: {domain} | IP address: {res} | Data de expiração: {exp_date} | issuer_name:{issuer_organization_name}')
                                        
            except:
                print(f'error while trying to connect in {domain}')
                pass      
        ssl_validation(domain)


#dictionary - armazenar informações. 
            
        #função para resolver o IP do host. 
            
            
   
       
        




    