#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle  nh;
int freq = 980; // Hz
int Left = 4;
int Right = 3;
int ledPin = 2;

void messageCb( const std_msgs::Float32& toggle_msg){
  analogWrite(ledPin, toggle_msg.data); //toggle_msg.data //mandar pines con high or low
  digitalWrite(Left, LOW);
  digitalWrite(Right, HIGH);
   
  
}
   
//
ros::Subscriber<std_msgs::Float32> sub("/cmd_pwm", &messageCb);



void setup()
{
  nh.initNode();
  pinMode(ledPin, OUTPUT);
  //ledcSetup(ledChannel, freq, 100); 
  //ledcAttachPin(ledPin, 10); 
  nh.subscribe(sub);


}

  


void loop()
{
    //ros::Subscriber<std_msgs::Float32> sub("cmd_pwm", &messageCb );


  


  //ledcWrite(ledChannel, dutyCycle);
  //delay(15);
  
  //str_msg.data = hello;
  //chatter.publish( &str_msg );
  nh.spinOnce();
  //delay(1000);
}

/*
#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh; // this helps ros to become a node
std_msgs::String str_msg;
ros::Publisher pub("chatter", &str_msg);

char hello[13] = "hello world!";

void setup() {
  // put your setup code here, to run once:
  nh.initNode();
  nh.advertise(pub);
}

void loop() {
  
  // put your main code here, to run repeatedly:
  str_msg.data = hello;
   chatter.publish( &str_msg );
   nh.spinOnce();
   delay(1000);

   
}
*/
