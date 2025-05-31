#!run as root and source /opt/ros/noetic/setup.bash
#!/usr/bin/env python
from pynput import keyboard
import rospkg
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from std_msgs.msg import Bool


#ros topics
#pub = rospy.Publisher('chatter', String, queue_size=10)
yaw = rospy.Publisher('yaw', UInt8, queue_size=5)
pitch = rospy.Publisher('pitch', UInt8, queue_size=5)
fire = rospy.Publisher('fire_laser', Bool, queue_size=5)

yaw_angle = 90.0
pitch_angle = 90.0
laser_state  = False

step = 1

#defining node
rospy.init_node('keyboard', anonymous=False)
rate = rospy.Rate(120) # Hz    

if __name__ == '__main__':
    try:
        
        

        while not rospy.is_shutdown():
            
            key = 'n'
            with keyboard.Events() as events:
                # Block at most one second
                event = events.get(1)
                events.get()
                if event is not None:
                    key = event.key.char

            


            if key == 'q': 
                break
            
            #pitch movement
            if key == 'w' and pitch_angle < 180:
                pitch_angle += step 
                pitch.publish(int(pitch_angle))
                rospy.loginfo(pitch_angle)
                
            if key == 's' and pitch_angle > 30: 
                pitch_angle -= step
                pitch.publish(int(pitch_angle))
                rospy.loginfo(pitch_angle)
                
            #yaw movement
            if key == 'a' and yaw_angle < 180: 
                yaw_angle += step
                yaw.publish(int(yaw_angle))
                rospy.loginfo(yaw_angle)
                
            if key == 'd' and yaw_angle > 0: 
                yaw_angle -= step
                yaw.publish(int(yaw_angle))
                rospy.loginfo(yaw_angle)
                
            
            #fire
            if key == 'f': 
                laser_state = not laser_state
                rospy.loginfo(f"fire {laser_state}")
                fire.publish(laser_state)

            rate.sleep()

            
            


    except rospy.ROSInterruptException:
        pass