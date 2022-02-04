#!/usr/bin/python3
import ssl
import argparse
import sys
import re
from datetime import date
from datetime import timedelta
from datetime import datetime
from cryptography import x509

# Method to get all certificates from the MY cert stores
def get_certs():
    certs = []
    for store in ["MY"]:
        for cert, encoding, trust in ssl.enum_certificates(store):
            certificate = x509.load_der_x509_certificate(cert, backend=None)
            certs.append(certificate)
    return certs

# Method that will use regex to extract cert subject - will use if I can figure out how to load certs into an array and return them to be shown in Icinga
def get_cert_name(cert):
    regex = "(?<=Name\()[a-zA-Z0-9-.=]*"
    sub = ""
    name = ""

    sub = str(cert.subject)
    name = re.findall(regex, sub)
    sub = str(name).strip("['']")

    # Icinga cannot process '=' as perf data, must remove it
    if "=" in sub:
        reg = "(?<==)[a-zA-Z0-9-.]*"
        name = ""

        name = re.findall(reg, sub)
        sub = str(name).strip("['']")

    return sub

__version__ = "1.0.0"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-V', '--version', action='version', version='%(prog)s v' + sys.modules[__name__].__version__)
    args = parser.parse_args()

# Initialize and declare variables
warn_threshold = timedelta(days=21)
crit_threshold = timedelta(days=7)
today = datetime.now()
expiring_certs = []
num_crit = 0
num_warn = 0

# Begin main method
certificate = get_certs()

# loop through list of certificates
for cert in certificate:
    # Evaluate certs to see if they're about to expire, and increment num_crit if less than 1 week from expiration, or num_warn if less than 3 weeks from expiration
    time_until_expiration = cert.not_valid_after - today
    if time_until_expiration < crit_threshold:
        num_crit += 1
        expiring_certs.append(cert)
    elif time_until_expiration < warn_threshold:
        num_warn += 1
        expiring_certs.append(cert)

# If any certs are about to expire in a week or less, throw critical and exit
if num_crit > 0:
    print("CRITICAL - %d certificate(s) already expired, or less than one week from expired |" % num_crit, end="")
    # Get performance data. Re-calculate time until expiration and then print the data as:
    # 'cert_subject'=days_until_expiration.
    #  This will allow icinga to display the cert and days until expiration in the performance data section
    for cert in expiring_certs:
        time_until_expiration = cert.not_valid_after - today
        print(" '" + str(get_cert_name(cert)) + "'=" + str(time_until_expiration.days), end="")
    exit(2)
# If any certs are about to expire in 3 weeks, throw warning and exit
elif num_warn > 0:
    print("WARNING - %d certificate(s) are less than two weeks from expiration |" % num_warn, end="")
    for cert in expiring_certs:
        time_until_expiration = cert.not_valid_after - today
        print(" '" + str(get_cert_name(cert)) + "'=" + str(time_until_expiration.days), end="")
    exit(1)
else:
    print("OK - There are no expiring certificates")
