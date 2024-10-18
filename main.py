import cv2
import requests
import time

# Set up camera
cap = cv2.VideoCapture(0)

# Initialize variables for motion detection
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# URL for ntfy.sh
ntfy_url = "ntfy.sh/K3R3wHq4w9mwcwNd"

def send_notification():
    payload = {
        'title': 'Motion Detected',
        'message': 'Motion detected by Raspberry Pi camera!',
        'priority': 'high'
    }
    try:
        response = requests.post(ntfy_url, json=payload)
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print("Failed to send notification.")
    except Exception as e:
        print(f"An error occurred: {e}")

while cap.isOpened():
    # Compute difference between two frames
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        send_notification()
        time.sleep(10)  # Wait for 10 seconds before sending another notification

    frame1 = frame2
    ret, frame2 = cap.read()

    # Press 'q' to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

