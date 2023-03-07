//Include the necessary libraries
#include <ros.h> //Library to use ROS commands
#include <std_msgs/Float32.h> //Library to use Float32 type data

ros::NodeHandle nh; //This command initialize the node

//We define the pins of the Arduino and save them in the variables
int enable = 2; //In the pin 2 we send the PWM value
//This pins define if the motor will go clockwise or or counterclockwise
int in1 = 3; //If we send HIGH it will go clockwise
int in2 = 4; //If we send High it will go counterclockwise

//We define the variable PWM where we will be storing the data received from the ROS node
float PWM = 0;

//In this function we receive the data of the ROS node and calculate how the motor should move
void message( const std_msgs::Float32& PWM1){ //We receive the topic in the PWM1 variable
  PWM = PWM1.data; //We store the topic in the PWM variable
    //We define how the code will normally start
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);
  if (PWM > 255){  //If the PWM value is greater than 255 (the max allowed) we only send 255 to the motor
    analogWrite(enable, 255);
  }
  else if (PWM<=0){  //If the PWM is less than or equal than 0 we invert movement of the motor
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enable, -1*PWM1.data); // Since the PWM is negative we can't send negative values we multiply it by -1
  }
  else if (PWM>0 and PWM<255){ //If PWM is greater than 0 and less than 255 it works normally
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enable, PWM1.data);
  }
  else if (PWM<-255){  // If PWM is less than -255 we invert the movement and send a constant 255
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enable, 255);
    
  }
}

// With this we subscribe to the ROS topic and send the data to the message function
ros::Subscriber<std_msgs::Float32> sub("/set_point", &message);

// Here the code is initialize and defined
void setup() {
  // put your setup code here, to run once:
  pinMode(enable, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  // We initialize the node and the subscribe
  nh.initNode();
  nh.subscribe(sub);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  
  delay(1);
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
