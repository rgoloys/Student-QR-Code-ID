import cv2
import time
from datetime import datetime
import pandas as pd
from tkinter import Tk
import atexit

# Initialize the camera
cap = cv2.VideoCapture(0)

# QRCode detector
detector = cv2.QRCodeDetector()

# Dictionary to track last scan time for each QR code
last_scan_time = {}
scan_interval = 15  # seconds
scanned_data = []  # List to store scanned data


def save_to_excel():
    # Save scanned data to Excel
    if scanned_data:
        df = pd.DataFrame(scanned_data,
                          columns=['ID', 'Name', 'Course', 'Year', 'Age', 'Address', 'Scan Date and Time'])
        df.to_excel('scanned_data.xlsx', index=False)
        print("Data saved to scanned_data.xlsx")
    else:
        print("No data to save")


def cleanup():
    save_to_excel()
    # Additional cleanup tasks can be performed here


# Register the cleanup function to be called on exit
atexit.register(cleanup)

# Create a Tkinter window
root = Tk()
root.title("QR Code Scanner")

# Hide the Tkinter root window
root.withdraw()


# Function to handle GUI and video capture
def main_loop():
    while True:
        ret, frame = cap.read()
        if ret:
            data, bbox, _ = detector.detectAndDecode(frame)
            current_time = time.time()  # Current time in seconds
            formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format date and time

            if data:
                # Check if QR code has been scanned before and if enough time has passed
                if data in last_scan_time:
                    time_since_last_scan = current_time - last_scan_time[data]
                    if time_since_last_scan < scan_interval:
                        # Skip processing if within interval
                        continue

                # Split data into fields
                fields = data.split('|')
                if len(fields) == 6:
                    student_id, name, course, year, age, address = fields
                    # Process the QR code
                    scanned_data.append([student_id, name, course, year, age, address, formatted_time])
                    print(f"Detected QR Code data:")
                    print(f"ID: {student_id}")
                    print(f"Name: {name}")
                    print(f"Course: {course}")
                    print(f"Year: {year}")
                    print(f"Age: {age}")
                    print(f"Address: {address}")
                    print(f"Scan Date and Time: {formatted_time}")
                    print('')
                    # Update the last scan time for this QR code
                    last_scan_time[data] = current_time

            # Display the image with bounding box if detected
            if bbox is not None:
                bbox = bbox.astype(int)  # Ensure bbox coordinates are integers
                for i in range(len(bbox)):
                    pt1 = tuple(bbox[i][0])
                    pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                    cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=2)

            cv2.imshow("QR Code Scanner", frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Start the video capture loop
if __name__ == "__main__":
    main_loop()
