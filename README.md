# windows_cert_check
A custom Icinga check written in Python to pull certs from the cert store and evaluate expiration.

# Purpose
This check was created because I could not find any SSL cert checks that would do what I needed. 

I have windows servers that I manage, and this check will:
  1. Reach into the cert store selected in the get_certs() function ("MY" in this case)
  2. Feed existing certificates into an array
  3. If any certificates exist, will evaluate them for expiration.
  4. If expiring within one week, or already expired, raise a critical alert in Icinga
  5. If expiring within three weeks, raise a warning in Icinga
  6. Evaluate as OK if no expiring certs exist
 
# Dependencies
The servers need python 3 (I tested with 3.9+) and the cryptography library. The cryptography library can be installed using pip.

# Setup: I will update this section later today or tomorrow - just created this repo

# Roadmap: I will update this section later today or tomorrow
