import requests

# Function to send notification using notify.sh
def send_notification():
    url = "http://<YOUR_RASPBERRY_PI_IP>:<PORT>/notify"  # Replace with your Raspberry Pi's IP and port
    payload = {
        "title": "Motion Detected!",
        "message": "Motion has been detected by the camera."
    }
    headers = {
        "Authorization": "Bearer <YOUR_API_TOKEN>"  # Replace with your API token
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Notification sent successfully!")
        else:
            print("Failed to send notification:", response.status_code, response.text)
    except Exception as e:
        print("Error sending notification:", e)

