#objects= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat',
#         9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 
#         16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 
#         25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 
#         33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
#         40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 
#         49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch',
#         58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
#         66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 
#         73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

import rospkg
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import UInt8
import cv2
from ultralytics import YOLO

#ros topics
#pub = rospy.Publisher('chatter', String, queue_size=10)
yaw = rospy.Publisher('yaw', UInt8, queue_size=5)
pitch = rospy.Publisher('pitch', UInt8, queue_size=5)
fire = rospy.Publisher('fire_laser', Bool, queue_size=5)

yaw_angle = 90.0
pitch_angle = 90.0
laser_state  = False

Kp_yaw = 0.02
Kp_pitch  = 0.01
Kd_pitch  = 0.001



#defining node
rospy.init_node('ObjectDetector', anonymous=False)
rate = rospy.Rate(10) # Hz  

yaw.publish(int(yaw_angle))
pitch.publish(int(pitch_angle))
fire.publish(laser_state)

##getting image source
cap = cv2.VideoCapture(2)
#image = cv2.imread("testImage.jpg")
ret, frame = cap.read()
if not ret:
    print('\n\nBIG ERROR CANNOT OPEN CAMERA !!\n\n')

frame_width = len(frame[0])
frame_hight = len(frame)
#print(frame_width, frame_hight)


# Load a model
model = YOLO("yolov8m.pt") 


x_error = 0
y_error = 0


while(True):

    ret, frame = cap.read()

    results = model(source=frame, show=False, conf=0.55, classes=[0], device= 0)  # predict on an image

    objects = results[0].boxes.xyxy.cpu().numpy()

    if len(objects) == 0:
        laser_state = False
        fire.publish(laser_state)
    #print(objects)

    for OOI in objects:

        center = [ int((OOI[0]+OOI[2])/2) , int((OOI[1]+OOI[3])/2) ]

        # Drawing lines to POIs
        cv2.circle(frame, center, 5, (0,0,255), -1)
        cv2.line(frame, center, (frame_width//2, center[1]), color=(0,0,255), thickness=2)
        cv2.line(frame, center, (center[0], frame_hight//2), color=(0,0,255), thickness=2)

        x_error = frame_width//2 - center[0]
        y_error = frame_hight//2 - center[1]

        print("\n\nERROR = ", x_error, "     ", y_error)

        
        # yaw movement
        if x_error < 0:
            if yaw_angle + x_error*Kp_yaw >= 45:
                yaw_angle = yaw_angle + x_error*Kp_yaw
                print(yaw_angle)
                yaw.publish(int(yaw_angle))
        
        elif x_error > 0:
            if yaw_angle + x_error*Kp_yaw <= 175:
                yaw_angle = yaw_angle + x_error*Kp_yaw
                print(yaw_angle)
                yaw.publish(int(yaw_angle))
        
        # pitch movement
        if y_error > 0:
            if pitch_angle - y_error*Kp_pitch >= 70:
                pitch_angle = pitch_angle - y_error*Kp_pitch
                print("Pitch angle: ",pitch_angle)
                pitch.publish(int(180-pitch_angle))
        elif y_error < 0:
            if pitch_angle - y_error*Kp_pitch <= 100:
                pitch_angle = pitch_angle - y_error*Kp_pitch
                print("Pitch angle: ",pitch_angle)
                pitch.publish(int(180-pitch_angle))

        
        # when to fire
        if abs(y_error) < 10 and abs(x_error) < 10:
            laser_state = True
            fire.publish(laser_state)
        else:
            laser_state = False
            fire.publish(laser_state)

    


        



    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    
    # Drawing the center lines
    cv2.line(frame, (frame_width//2, 0), (frame_width//2, frame_hight), color=(127,127,127), thickness=1)
    cv2.line(frame, (0, frame_hight//2), (frame_width, frame_hight//2), color=(127,127,127), thickness=1)
    
    cv2.imshow("el7a2oona", frame)

    

cap.release() 
cv2.destroyAllWindows() 
