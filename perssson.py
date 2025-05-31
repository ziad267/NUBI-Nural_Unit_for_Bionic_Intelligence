import rospkg
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from ultralytics import YOLO
import cv2

#ros topics
#pub = rospy.Publisher('chatter', String, queue_size=10)
yaw = rospy.Publisher('yaw', UInt8, queue_size=5)
pitch = rospy.Publisher('pitch', UInt8, queue_size=5)
fire = rospy.Publisher('fire_laser', Empty, queue_size=5)

yaw_angle = 90.0
pitch_angle = 90.0

step = 1

#defining node
rospy.init_node('PersonDetector', anonymous=False)
rate = rospy.Rate(10) # Hz  

cap = cv2.VideoCapture(2)
ret, frame = cap.read()

frame_width = len(frame[0])
frame_hight = len(frame)

# Load a model
model = YOLO("yolov8n-pose.pt")  # load a pretrained model (recommended for training)

while(True):

    ret, frame = cap.read()


    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

    results = model(source=frame, show=False, conf=0.8, device=0)  # predict on an image
    
    #POIs 6,5,12,11 
    people = results[0].keypoints.xy.numpy()
    #print(people)
    
    

    for person in people:

        if len(person) != 0:
            #right shoulder
            cv2.circle(frame, (int(person[6][0]), int(person[6][1])) , 5, (0,0,255), -1)
            #left shoulder
            cv2.circle(frame, (int(person[5][0]), int(person[5][1])) , 5, (0,0,255), -1)
            #left hip
            cv2.circle(frame, (int(person[11][0]), int(person[11][1])) , 5, (0,0,255), -1)
            #right hip
            cv2.circle(frame, (int(person[12][0]), int(person[12][1])) , 5, (0,0,255), -1)

            points = [person[6], person[5], person[11], person[12]]

            good_points =0
            for point in points:
                if 0 not in point:
                   good_points += 1

            

            #because cant divide by zero :)
            if good_points != 0:
                target = [int((person[5][0]+person[6][0]+person[11][0]+person[12][0])/good_points),
                        int((person[5][1]+person[6][1]+person[11][1]+person[12][1])/good_points)]
            
                print(target)
                yaw.publish(int(180-180*target[0]/frame_width))
                pitch.publish(int(130*target[1]/frame_hight))               
            

                #draw the crossair
                cv2.line(frame, (target[0]+10, target[1]), (target[0]-10, target[1]),(255,0,0), 3)
                cv2.line(frame, (target[0], target[1]+10), (target[0], target[1]-10),(255,0,0), 3)
        
    

    cv2.imshow('frame', frame)



    


cap.release() 
cv2.destroyAllWindows() 
