
// ESP laser   D0   16
// ESP yaw     D1   5
// ESP pitch   D2   4


#include <Servo.h>

#include <ros.h>
#include <std_msgs/UInt8.h>
#include <std_msgs/Bool.h>
 
ros::NodeHandle nh;


Servo yaw_servo;
Servo pitch_servo;

#define laser 16 //D0

/////////////////////////////////Subscribers Call Back///////////////////////////////////

void fire_cb( const std_msgs::Bool& toggle_msg){
    if(toggle_msg.data){
      digitalWrite(laser, HIGH);
    }else{
      digitalWrite(laser, LOW);
    }  

}

void yaw_cb( const std_msgs::UInt8& yaw_angle){
   yaw_servo.write(yaw_angle.data);
}

void pitch_cb( const std_msgs::UInt8& pitch_angle){
   pitch_servo.write(pitch_angle.data);
}

////////////////////////////////////Topic Protoypes////////////////////////////


ros::Subscriber<std_msgs::Bool> sub_fire("fire_laser", &fire_cb );
ros::Subscriber<std_msgs::UInt8> sub_yaw("yaw", &yaw_cb );
ros::Subscriber<std_msgs::UInt8> sub_pitch("pitch", &pitch_cb );






void setup()
{
  yaw_servo.attach(5);
  yaw_servo.write(90);
  pitch_servo.attach(4);
  pitch_servo.write(90);
  
  pinMode(laser, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);


  nh.initNode();

  nh.subscribe(sub_fire);
  nh.subscribe(sub_yaw);
  nh.subscribe(sub_pitch);
}

void loop()
{

  nh.spinOnce();
  delay(50);
}
