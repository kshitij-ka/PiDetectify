#!/bin/bash

PROJECT_DIR=/home/$(whoami)/iot-mini

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3.11-venv python3-picamera2 python3-opencv # Python
sudo apt install -y build-essential cmake pkg-config # Developer tools and packages
sudo apt install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev # Image I/O packages
sudo apt install -y libgtk2.0-dev libcap-dev # GTK development library & picamera2 dependency
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev # Video I/O packages
sudo apt install -y libatlas-base-dev gfortran # Optimize OpenCV operation


cd $PROJECT_DIR
python3 -m venv .
source $PROJECT_DIR/bin/activate
pip install numpy opencv-python picamera picamera2 # for camera vision 
pip install requests # for notifications
pip install virtualenvwrapper # virtual env
wget https://github.com/opencv/opencv/archive/refs/tags/4.10.0.tar.gz
tar -xvf 4.10.0.tar.gz
cd opencv-4.10.0/
mkdir build/
cd build/
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON ..
make # For compiling OpenCV
sudo make install
sudo ldconfig
