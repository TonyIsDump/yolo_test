from ultralytics import YOLO
import cv2
import math 
import serial
import time
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
arduinoData = serial.Serial("/dev/ttyACM0", 115200)

def send_coordinates_to_arduino(x, y):
    # Convert the coordinates to a string and send it to Arduino
    coordinates = f"{x},{y}\r"
    #signal = "true"
    #arduinoData.write(signal.encode())
    arduinoData.write(coordinates.encode())
    print(f"X{x}Y{y}\n")


# model
model = YOLO("runs/detect/train/weights/best.pt") 
# object classes
classNames = ["person"]


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # class name
            cls = int(box.cls[0])
            classname = classNames[cls]
            
            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 255, 255)
            thickness = 1
            if classname == "person":
                if abs(x2 - x1) > 300:
                    x = (x1 + x2)/2
                    y = (y1 + y2)/2
                    #print("Class name -->", classNames[cls])
                    #print(x,y)
                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                    
                    #signal = f" 12331 "  # send serial data
                    #print(type(signal))
                 #   arduinoData.write(signal.encode())
                    send_coordinates_to_arduino(x, y)

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
