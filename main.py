from picamera2 import Picamera2
import cv2
import numpy as np
import time
import requests
from datetime import datetime

# ntfy.sh topic (choose your unique topic name)
ntfy_topic = "K3R3wHq4w9mwcwNd"  # Replace with your ntfy.sh topic
ntfy_url = f"https://ntfy.sh/{ntfy_topic}"

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
picam2.start()

time.sleep(2)  # Give the camera some time to initialize

# Read the initial frames
frame1 = picam2.capture_array()
frame2 = picam2.capture_array()

motion_detected = False

while True:
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)
    
    # Convert the difference to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the blurred image to highlight the motion
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in holes
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours (motion areas) in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # If motion is detected and not already notified, send a notification
        if not motion_detected:
            current_time = datetime.now().strftime("%H:%M:%S")  # Get current time
            message = f"Motion detected in room at {current_time}"  # Format message

            print("Motion detected! Sending notification...")
            try:
                response = requests.post(
                    ntfy_url,
                    json={"message": message}  # Send only the message
                )
                if response.status_code == 200:
                    print("Notification sent successfully!")
                else:
                    print(f"Failed to send notification. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error sending notification: {e}")
            
            motion_detected = True

    # If no contours are found, reset the motion_detected flag
    if len(contours) == 0:
        motion_detected = False

    # Display the result
    cv2.imshow("Motion Detection", frame1)

    # Update frames: frame1 becomes frame2, and a new frame is read as frame2
    frame1 = frame2
    frame2 = picam2.capture_array()

    # Press 'q' to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources and close all OpenCV windows
picam2.stop()
cv2.destroyAllWindows()

