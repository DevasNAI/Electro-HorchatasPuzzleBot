//  Include the necessary libraries
#include <ros.h> //Library to use ROS commands
#include <std_msgs/Float32.h> //Library to use Float32 type data

//  This command initialize the node
ros::NodeHandle nh; 

//  Arduino Pin definition
//  PWM Pin
int enable = 2;
//  HIGH and LOW Motor pins
int in1 = 3;
int in2 = 4;

//  Variable that will store /set_point  ROS Topic's value
float PWM = 0;

//In this function we receive the data of the ROS node and calculate how the motor should move
/**
 * @brief Receives a message from a ROS Topic (a PWM signal) and defines motor behavior depending on its value.
 * If the message is negative, the motor direction is inverted. The motor will spin at the message's value.
 * 
 * @param PWM1 ROS /set_point value
 */
void message( const std_msgs::Float32& PWM1)
{
  //  Argument is stored in PWM Variable
  PWM = PWM1.data; 
  //  Motor initial behavior
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);

  //  Bounds the motor's maximum operation value
  if (PWM > 255){  
    analogWrite(enable, 255);
  }
  //  If the PWM is less than or equal than 0, the motor is inverted
  else if (PWM<=0)
  {  
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    //  The PWM signal can't be negative, so it is converted back to positive
    analogWrite(enable, -1*PWM1.data);
  }
  //  If PWM is in the range of 0 and 255, it behaves normally
  else if (PWM>0 && PWM<255)
  { 
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enable, PWM1.data);
  }
  // If PWM is less than -255 we invert the movement and send the maximum PWM Value
  else if (PWM<-255)
  {  
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enable, 255);
    
  }
}

// With this we subscribe to the ROS topic and send the data to the message function
ros::Subscriber<std_msgs::Float32> sub("/set_point", &message);

// Arduino pin setup and Node initialization
void setup() {
  //  H-Bridge pin setup
  pinMode(enable, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  //  Motor node initialization
  nh.initNode();
  //  Node subscription to topic /set_point
  nh.subscribe(sub);
  
}

void loop() {
  // Runs the code
  nh.spinOnce();
  
  delay(1);
}
