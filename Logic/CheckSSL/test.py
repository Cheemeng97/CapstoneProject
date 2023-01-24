from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna

from socket import socket
from collections import namedtuple

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

    issuer = get_issuer(hostinfo.cert)
    validFrom = hostinfo.cert.not_valid_before
    validTo = hostinfo.cert.not_valid_after

    if issuer != None & validFrom != None & validTo != None:
        print("SSL Certificate is valid")

    if "DigiCert" | "GeoTrust" | "Thawte" | "RapidSSL" | "Symantec" | "VeriSign" | "Comodo" | "GoDaddy" | "GlobalSign" | "Entrust" | "StartCom" | "Trustwave" | "Buypass" | "Certum" | "IdenTrust" | "Let's Encrypt" in issuer:
        print("SSL Certificate is issued by a trusted CA")
    else:
        print("SSL Certificate is not issued by a trusted CA")

    # s = '''» {hostname} « … {peername}
    # \tcommonName: {commonname}
    # \tSAN: {SAN}
    # \tIssuer: {issuer}
    # \tValid From: {notbefore}
    # \tValid To:  {notafter}
    # '''.format(
    #         hostname=hostinfo.hostname,
    #         peername=hostinfo.peername,
    #         commonname=get_common_name(hostinfo.cert),
    #         SAN=get_alt_names(hostinfo.cert),
    #         issuer=get_issuer(hostinfo.cert),
    #         notbefore=hostinfo.cert.not_valid_before,
    #         notafter=hostinfo.cert.not_valid_after
    # )
    # print(s)

def check_it_out(hostname, port):
    hostinfo = get_certificate(hostname, port)
    analyseSSLCert(hostinfo)


import concurrent.futures
# if __name__ == '__main__':

def SSL_Checker(urlInput):
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        # for hostinfo in e.map(lambda x: get_certificate(x[0], x[1]), urlInput):

    hostinfo = get_certificate(urlInput, 443)
    analyseSSLCert(hostinfo)