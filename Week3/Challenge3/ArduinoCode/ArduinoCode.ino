#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

int enable = 2;
int in1 = 3;
int in2 = 4;

float PWM = 0;

void message( const std_msgs::Float32& PWM1){
  PWM = PWM1.data;
  analogWrite(enable, PWM1.data);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  if (PWM > 255){
    PWM = 255;
  }
  else if (PWM<0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
    
}

ros::Subscriber<std_msgs::Float32> sub("/set_point", &message);

void setup() {
  // put your setup code here, to run once:
  pinMode(enable, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  nh.initNode();
  nh.subscribe(sub);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  
  delay(1);
}
