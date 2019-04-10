# bytebuffercollector
Collects byte buffer statistics and connection statistics from a SonicWall firewall via SSH management

This tool automatically collects the '1500 byte buffer' and connection (peak/curr/max) statistics from a SonicWall firewall.

# Setup:
 1. Install the latest version of Python 3.
 2. Use 'pip' or 'pip3' to install the necessary modules.
	-- pip install paramiko
	-- pip install datetime
	-- pip install schedule
	-- I believe the 'time' module is part of the standard library.
 3. In this script, configure the IP, SSH mgmt port, and management credentials below.
 4. Set 'scheduleTimer' to a desired interval in seconds (300 by default). Save the changes.
 5. Launch the script from the command line (py bytebuffercollector.py)
