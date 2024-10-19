# IoT Mini Project - 2024

This mini project uses picamera to detect motion, upon detecting motion, it sends notification to devices subscribed to the channel using ntfy.sh

---

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
git clone https://git.kska.io/notkshitij/iot-mini.git
```

2. Change current working directory:
```shell
cd ./iot-mini
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
    docker run -it ghcr.io/wg-easy/wg-easy wgpw <PASSWORD-HERE>
    ```

    This will return a `PASSWORD_HASH`

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

9. Check if ntfy.sh is setup correctly:
    - Visit `<RASPBERRYPI-IP>:80` from a browser. Make sure Raspberry Pi and the other device are on the same network. On Raspberry Pi, you can visit `localhost:8080`
    - If you see a dashboard, it implies Docker and ntfy.sh were setup correctly.

10. In ntfy.sh dashboard, in the left menu at the bottom, click on `Subscribe to topic`, and specify the topic name: `motion-sensing`

> [!NOTE]
> Make sure you're in the directory where you cloned this repo while running all these commands.
