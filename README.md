# PiDetectify

This project utilizes [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) for processing and [Pi Camera](https://www.raspberrypi.com/documentation/accessories/camera.html) to detect motion. Upon detecting motion, it sends a notification to the user via [ntfy.sh](https://ntfy.sh). If the user is not on the same network as the Raspberry Pi, notifications are sent over a VPN using a [WireGuard tunnel](https://www.wireguard.com). Both ntfy and WireGuard run within their own separate [Docker](https://www.docker.com) containers, and everything runs locally.

> [!NOTE]
> I created this for my college project. I do not plan on adding more features to it. If you encounter any bugs, feel free to create an [issue](https://git.kska.io/notkshitij/PiDetectify/issues/new) (I am more active on [KSKA Git](https://git.kska.io/notkshitij/PiDetectify) than on [GitHub](https://github.com/kshitij-ka/PiDetectify).)

---

## Read detailed description in [ABOUT.md](ABOUT.md).

## Demo images

Motion Detection Window | Notification Sent | Notification Received
--- | --- | ---
![Motion](Demo/Motion%20Detection%20Window.png) | ![Sent](Demo/Notification%20Sent.png) | ![Received](Demo/Notification%20Received.jpeg)

## Prerequisites:
1. Raspberry Pi (only tested on 3B+, should work on 2/4/5 as well)
2. Pi Camera
3. Internet connection
4. Raspberry Pi OS **64-bit**

> [!IMPORTANT]
> USE 64-BIT OS FOR FASTER PROCESSING.

## Steps to setup

1. Clone this repository:
```shell
git clone https://git.kska.io/notkshitij/PiDetectify.git
```

2. Change current working directory:
```shell
cd ./PiDetectify
```

3. Run `setup.sh`:
```shell
./setup.sh
```

4. Setup firewall on Raspberry Pi:
```shell
sudo apt install -y ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow 22 # for ssh
sudo ufw allow 80 # for ntfy
sudo ufw allow 51821/tcp # wireguard tcp
sudo ufw allow 51820/udp # wireguard udp
sudo ufw status numbered
sudo ufw enable
sudo systemctl start ufw
sudo systemctl enable ufw
```

5. Setup Wireguard:

    - Generate bcrypt password hash by running:
    ```shell
    docker run -it ghcr.io/wg-easy/wg-easy wgpw '<PASSWORD_HERE>'
    ```

    This will return a `PASSWORD_HASH`. For addition information, checkout their [guide](https://github.com/wg-easy/wg-easy).

    - Create a file in the current directory called `.env`

    - Add the following values in `.env` file:
    ```env
    PASS='<PASSWORD_HASH generated here>'
    IP=<PUBLIC IP>

    # Inside single quotations, paste the password hash for PASS variable
    # Get your public IP by using something like http://ip.me, and paste your public IP there
    ```

8. Create and run the containers:
```shell
docker compose up -d
```

9. Check if ntfy.sh and wireguard tunnel is setup correctly:

    - Visit `<RASPBERRYPI-IP>:80` from a browser. Make sure Raspberry Pi and the other device are on the same network. On Raspberry Pi, you can visit `localhost:8080`

    - If you see a dashboard, it implies Docker and ntfy.sh were setup correctly.

    - Visit `<RASPBERRYPI-IP>:51821`, enter the password which you specified in the beginning (NOT the password hash, the password).

    - Add new clients to remotely connect and receive notifications.

10. In ntfy.sh dashboard, in the left menu at the bottom, click on `Subscribe to topic`, and specify the topic name: `motion-sensing`

11. Lastly, run the `main.py` file to view motion detection window on screen and send notifications on detecting motion:
```shell
python3 main.py
```

> [!NOTE]
> Make sure you're in the directory where you cloned this repo while running all these commands.

---
