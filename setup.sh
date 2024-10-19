#!/bin/bash

line="=================================="

###############################################

# Install dependencies
sudo apt update

# Checking for python and it's dependencies
if ! dpkg -l | grep -q "python3"; then
	echo -e "$line\npython3 not installed, installing...\n$line\n"
	sudo apt install -y python3
else
	echo -e "$line\npython3 already installed. Moving one...\n$line\n"
fi
if ! dpkg -l | grep -q "python3-pip"; then
	echo -e "$line\npython3-pip not installed, installing...\n$line\n"
	sudo apt install -y python3-pip
else
	echo -e "$line\npython3-pip already installed. Moving one...\n$line\n"
fi
if ! dpkg -l | grep -q "python3.11-venv"; then
	echo -e "$line\npython3.11-venv not installed, installing...\n$line\n"
	sudo apt install -y python3.11-venv
else
	echo -e "$line\npython3-venv already installed. Moving one...\n$line\n"
fi

# Install camera stuff
echo -e "$line\nInstalling camera dependencies\n$line"
sudo apt install -y python3-picamera2 python3-picamera python3-opencv python3-numpy # Python camera packages for pi camera
sudo apt install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev # Image I/O packages
sudo apt install -y libgtk2.0-dev libcap-dev # GTK development library & picamera2 dependency
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev # Video I/O packages
sudo apt install -y libatlas-base-dev gfortran # Optimize OpenCV operation

sudo apt install -y python3-requests # For notifications

###############################################

echo -e "$line\nSetting up Docker\n$line"
./docker-setup.sh
echo -e "$line\nDocker installation complete\n$line"

