# About
- Project uses Python for motion sensing using the camera
	- Uses picamera, opencv, numpy libraries for processing the camera feed and motion detection
	- Uses requests library for sending notification
- Docker for running 2 containers:
	- ntfy for notifications and dashboard (supports PUB/SUB too!)
	- wireguard for encrypted tunnel (didn't test since my router has CG-NAT)
	
# Features
	- Scanning the camera feed and processing all done locally, therefore no 3rd party, hence privacy and security preserved
	- Docker for isolation of notifications and encrypted tunnel
	- Entire setup secured using ufw firewall
	
