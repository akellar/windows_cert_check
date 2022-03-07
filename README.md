# windows_cert_check
A custom Icinga check written in Python to pull certs from the cert store and evaluate expiration.

# Purpose
This check was created because I could not find any SSL cert checks that would do what I needed. 

I have windows servers that I manage, and this check will:
  1. Reach into the cert store selected in the get_certs() function ("MY" in this case)
  2. Feed existing certificates into an array
  3. If any certificates exist, will evaluate them for expiration.
  4. Parse arguments to get critical threshold, compare timedelta objects created for cert and this threshold, and if needed throw critical alert in Icinga
  5. Parse arguments to get warning threshold, compare timedelta objects created for cert and this threshold, and if needed throw a warning in Icinga
  6. Evaluate as OK if no expiring certs exist
 
# Dependencies
The servers need python 3 (I tested with 3.9+) and the cryptography library. The cryptography library can be installed using pip.

# Setup: 
  1. Install Python 3.9+ either directly or via chocolatey
  2. Install the cryptography library with pip
  3. Clone repo onto the target machine that will run the check. This check will be run by the agent on the windows machine
  5. Create a command in Icinga that will identify the compiler on your windows machine and location of the windows_cert_check.py file
  6. Create a service check and use the command created as the check command

Quick note on this setup: I used the Icinga Director to set up the check command and service. The Director makes it much easier than having to set up the check and service via the CLI. I would recommend, if you haven't imported the Director, that you do this and familiarize yourself prior to installing the check.

# Roadmap: 
1. Make the setup a bit more descriptive, with some screenshots included. I need to spin up a lab environment at home and get everything running in order to do this. 
