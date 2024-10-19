#!/bin/bash

###############################################
line="=================================="

# Remove conflicting packages
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Setup Docker's apt repo
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker.socket
sudo systemctl enable docker.socket
sudo systemctl start containerd.service
sudo systemctl enable containerd.service

# Test
sudo docker run hello-world

# Use docker without sudo
sudo groupadd docker
sudo usermod -aG docker $USER
sudo chown $USER:docker /var/run/docker.sock

# Show running containers
docker ps -a

echo -e "\n$line"
echo -e "Docker setup complete."
echo -e "## Designed and Engineered by Kshitij"
echo -e "$line\n"
