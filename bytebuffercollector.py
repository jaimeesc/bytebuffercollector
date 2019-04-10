# This tool automatically collects the '1500 byte buffer'
# 	and connection (peak/curr/max) statistics from a SonicWall firewall.
#
# Setup:
# 1. Install the latest version of Python 3.
# 2. Use 'pip' or 'pip3' to install the necessary modules.
#	-- pip install paramiko
#	-- pip install datetime
#	-- pip install schedule
#	-- I believe the 'time' module is part of the standard library.
# 3. In this script, configure the IP, SSH mgmt port, and management credentials below.
# 4. Set 'scheduleTimer' to a desired interval in seconds (300 by default). Save the changes.
# 5. Launch the script from the command line (py bytebuffercollector.py)
#
# Built on 4-9-2019

# Import these modules
import paramiko # Used for SSH client communication
import time # Used for the sleep functionality
from datetime import datetime, timezone # Used for the generateTimestamp() function.
import schedule # Used for managing the scheduled routine

# Firewall login information
fwIp = '192.168.0.3' # Enter the IP of the firewall.
fwSshPort = '22' # Enter a custom SSH port if needed.
fwUser = 'admin' # Enter the user name between the ''.
fwPass = 'password' # Enter the password between the ''.

# Configure how often to SSH in and pull the buffer and connection information.
scheduleTimer = 300 # Seconds

# Function to generate a timestamp.
def generateTimestamp():
	currentTime = datetime.now(timezone.utc).astimezone()
	currentTime = str(currentTime)
	return currentTime

# This is the routine that pulls and displays the 1500 byte buffer statistics
# and the connection information (peak, current, and max)
def routine():
	try:
	# SSH connection setup.
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(fwIp, port=fwSshPort, username=fwUser, password=fwPass, look_for_keys=False)
	# Creates a channel.
		sendchannel = client.invoke_shell()
		print("--", generateTimestamp(), "--")
	# Send the command.
		sendchannel.sendall('\nshow tech-support-report intrusion-detection-prevention\r\n\n\n\n\n\n\n\n\n\n\n\n q')
	# Sleep for 2 seconds to wait for the response data.
	# Sleeping for 2 sec to give the response enough time to come in.
		time.sleep(2)
	# Pull the received data from the channel and decode, then split it into a list object
		sc = sendchannel.recv(7500)
		sc = sc.decode('ASCII')
		sc = sc.split('\r')
	#	sc = sc.split('--MORE--[8D[K')
	# Iterate through the received data list object, and print out the buffer statistics
		for i in sc:
			if "1500 byte buffer count" in i:
				print(str(i).lstrip('--MORE--[8D[K'))
	# Send the next command.
		sendchannel.sendall('\rshow status\r q \r \n')
	# Sleep for 1 second to receive data.
	# Only sleeping 1 second because the expected data is in a much smaller response.
		time.sleep(1)
	# Pull the received data from the channel. Decode and split it.
		sc = sendchannel.recv(6000)
		sc = sc.decode('ASCII')
		sc = sc.split('\r')
	# Iterate through the response data. Print out the connection statistics.
		for i in sc:
			if "Connections:" in i:
				print(i.replace("  ", ""))
	# Close the channel
		sendchannel.close()
		print("\n\n")
	finally:
	# Close the SSH client connection.
		client.close()

# This function starts the schedule timer and runs the routine.
def startRoutine():
	schedule.every(scheduleTimer).seconds.do(routine)
	while True:
		schedule.run_pending()
		time.sleep(1)	

# Starts the scheduled routine on launch of the script.
# Runs the routine once initially before starting the loop.
if __name__ == '__main__':
	routine()
	startRoutine()
