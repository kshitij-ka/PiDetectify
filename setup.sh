#!/bin/bash

PROJECT_DIR=/home/$(whoami)/iot-mini

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-opencv python3-opencv

cd $PROJECT_DIR
python3 -m venv .
source $PROJECT_DIR/bin/activate
pip install requests
