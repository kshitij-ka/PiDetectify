import cv2
import numpy as np
import os
import time
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

# Initialize the camera
cap = cv2.VideoCapture(0)

# Read the first frame
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while True:
    # Calculate the difference between the frames
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check for motion
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Adjust the threshold as needed
            continue
        send_notification()
        break  # Exit after sending notification

    # Update frames
    frame1 = frame2
    ret, frame2 = cap.read()

    # Display the video feed (optional)
    cv2.imshow("Motion Detection", frame1)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

