import sys
from client_connect import ssl_validation

if len(sys.argv) < 2:
    print("usage => python3 app.py domain_list.txt")
    exit(0)
else:
    try:
        cert = ssl_validation()
        print(cert)
    except:
       print('error')
       pass
