# About

This file contains description about this project.

---

## What?

This project utilizes Raspberry Pi with Pi Camera to detect motion in real-time. When motion is detected, the system sends a notification to a specified topic on an ntfy.sh server. The setup involves several components, including a camera interface, Docker setup for ntfy.sh and WireGuard VPN, and a Python script for motion detection.

---

## Features

- **Local Camera Feed Processing**: The entire camera feed is scanned and processed locally on the device. No third-party services are involved, ensuring privacy and security are preserved.
- **Docker-Based Isolation**: The notification system and encrypted tunnel (via WireGuard) are containerized using Docker, providing better isolation, security, and ease of deployment.
- **Enhanced Security with UFW Firewall**: The entire setup is secured using UFW (Uncomplicated Firewall), ensuring that only necessary services are accessible and protecting the system from unauthorized access.

## Structure

1. `setup.sh`: A shell script to install dependencies and set up the environment.
2. `docker-setup.sh`: A shell script that installs Docker and its dependencies.
3. `docker-compose.yaml`: Docker Compose configuration to run ntfy.sh and WireGuard VPN in containers.
4. `main.py`: The Python script that captures camera frames, detects motion, and sends notifications.


---

### setup.sh

- Install `python3`, `pip`, and necessary libraries.
- Install camera libraries such as `picamera2`, `opencv`, and image processing libraries.
- Install `requests` for HTTP notifications.
- Set up Docker and start the `ntfy.sh` container using the [docker-setup.sh](docker-setup.sh) script.

## docker-setup.sh

- Remove any conflicting Docker packages.
- Add Docker’s official apt repository and install Docker and Docker Compose.
- Set up the `ntfy.sh` and `wg-easy` containers using the provided [docker-compose.yaml](docker-compose.yaml).
- Ensure Docker runs without sudo (add the current user to the Docker group).
- Test the Docker installation by running a "hello-world" container.

> [!NOTE]
> I have referred [official Docker documentation](https://docs.docker.com/engine/install/debian/) for this.

## docker-compose.yaml

- `ntfy`: The container running ntfy.sh for sending notifications.

  - Exposes port 80 and uses the `binwiederhier/ntfy` Docker image.
  - Configured with timezone IST and persistent storage for cache and config.

`wg-easy`: A WireGuard VPN container that allows secure access to the Raspberry Pi.

  - Exposes ports `51820/udp` and `51821/tcp`.
  - Uses environment variables for configuration and requires a password hash for login.

> [!TIP]
> Refer official documentation for [ntfy.sh](https://docs.ntfy.sh/install/#docker) and [Wireguard](https://github.com/wg-easy/wg-easy).

## main.py

- Initialize the Raspberry Pi camera using the `picamera2` library.
- Capture and compare two consecutive frames to detect motion using OpenCV’s frame difference method.
- If motion is detected, the script will send a notification to the configured `ntfy.sh` topic (`motion-sensing` in this case by default).

> [!TIP]
> You can customize the topic name in the `main.py` file by modifying the `ntfy_topic` variable. If you are using the local Docker instance for `ntfy.sh`, the script will use `localhost:80` by default. You can change that too by modifying the `rpi_ip` variable.

## Customization

- **Motion Detection Sensitivity**: The motion detection sensitivity can be adjusted by modifying the area threshold in the `cv2.contourArea(contour)` condition in `main.py`. Decrease the threshold to detect smaller movements or increase it to filter out smaller motion.
- **ntfy.sh Topic**: The topic for notifications is defined in `main.py` as `ntfy_topic`. You can change this to any unique topic name you want to receive notifications under.

---
