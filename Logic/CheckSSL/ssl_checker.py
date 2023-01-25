from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna

from socket import socket
from collections import namedtuple
from datetime import datetime

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')

HOSTS = [
    ('test-ev-rsa.ssl.com', 443), #valid SSL
    ('expired-rsa-dv.ssl.com', 443), #expired SSL
    ('revoked-rsa-dv.ssl.com', 443), #revoked SSL
    ('test.com', 443), #no SSL
]

def verify_cert(cert, hostname):
    # verify notAfter/notBefore, CA trusted, servername/sni/hostname
    cert.has_expired()
    # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
    # issuer

def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)

def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def analyseSSLCert(hostinfo):
    print("Analyzing SSL Certificate for: " + hostinfo.hostname)

    issuer = get_issuer(hostinfo.cert)
    validFrom = hostinfo.cert.not_valid_before
    validTo = hostinfo.cert.not_valid_after

    # check null
    print("Checking if SSL Certificate is null")
    result_nullCheck = "Not found"
    if issuer != None:
        result_nullCheck = "SSL Certificate found"

    # check trusted issuer
    print("Checking if SSL Certificate is trusted")
    result_trustIssuer = "Not Trusted"
    if "DigiCert" or "GeoTrust" or "Thawte" or "RapidSSL" or "Symantec" or "VeriSign" or "Comodo" or "GoDaddy" or "GlobalSign" or "Entrust" or "StartCom" or "Trustwave" or "Buypass" or "Certum" or "IdenTrust" or "Let's Encrypt" in issuer:
        result_trustIssuer = "Trusted"
    else:
        result_trustIssuer = "Not Trusted"

    # check valid from
    print("Checking if SSL certificate valid from")
    result_validFrom = "Invalid"
    if validFrom < datetime.now():
        result_validFrom = "Valid"
    else:
        result_validFrom = "Invalid"

    # check valid to
    print("Checking if SSL certificate valid to")
    result_validTo = "Invalid"
    if validTo > datetime.now():
        result_validTo = "Valid"
    else:
        result_validTo = "Invalid"

    


    #result
    data = {
        "result_NullCheck": result_nullCheck,
        "CommonName": get_common_name(hostinfo.cert),
        "SAN": get_alt_names(hostinfo.cert),
        "Issuer": issuer,
        "result_TrustIssuer": result_trustIssuer,
        "ValidFrom": str(validFrom),
        "result_ValidFrom": result_validFrom,
        "ValidTo": str(validTo),
        "result_ValidTo": result_validTo
    }

    #save to json
    import json
    with open('./Results/ssl_result.json', 'w') as outfile:
        json.dump(data, outfile)

def check_it_out(hostname, port):
    hostinfo = get_certificate(hostname, port)
    analyseSSLCert(hostinfo)

def SSL_Checker(urlInput):
    hostinfo = get_certificate(urlInput, 443)
    analyseSSLCert(hostinfo)