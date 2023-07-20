#include <ros.h>
#include <std_msgs/Float32.h>
#include  <Wire.h>
#include  <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2); 

ros::NodeHandle nh;
int pwm = 2;
int in1 = 3;
int in2 = 4;
// Encoder Pins
int encoderInterrupt = 19;
int encoderDirection = 18;
//  Pulse count that increases or decreases depending on rotation of the encoder
volatile long pulsecount = 0;

volatile bool direction = false;
// Pulses per revolution
int pulsesPerREV = 12;

// Counters for  during interval
long previousTime = 0;
 
// Variable for RPM measuerment
float rpm = 0;
 
// Variable for angular velocity measurement
float ang_velocity = 0;
float ang_velocity_deg = 0;

//  Constants for measurement conversion
const float rpm_to_radians = 0.10471975512;
const float rad_to_deg = 57.29578;
//  Moving average filter
float movingAvg[10];
int index = 0;
float avg = 0.0;
long prevT = 0;

/**
 * Message Callback
 * This function sends the motor the signal and direction it requires to move
 * @const std_msgs::Float32 message | It's a speed value from 1 to -1. 
 */
void messageCb( const std_msgs::Float32& message){
  int speed = message.data * 255;
  if (speed >= 0 && speed <= 255) {
    analogWrite(pwm, speed);   // turn the motor
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else if (speed < 0 && speed >= -255) {
    analogWrite(pwm, -1*speed);   // turn the motor
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);// change the orientation
  }
  else if (speed > 255){
    analogWrite(pwm, 255);   // turn the motor
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else {
    analogWrite(pwm, 255);   // turn the motor
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
}
//  Ros subscriber to topic
ros::Subscriber<std_msgs::Float32> sub("/motor_input", &messageCb);

/**
 * Motor pulse's lecture
 * Reads the speed of the motor and it stores it as RPM while
 * it applies a Moving Average Filter
 */
void motor_pulse()
{
 //  Gets current time 
  long currentTime = micros();
 //  Gets actual time
  long time = currentTime - previousTime;
  //  Reads the direction of the encoder
  int val = digitalRead(encoderDirection);
 //  If reading is 0, direction is Forward
  if(val == LOW) {
    //Forward
    direction = true;
  }
   //  Else, direction is reverse
  else {
    //Reverse
    direction = false;
  }

  //  If motor is moving, assigns positive or negative value of RPM's
  if (direction)
  {
   //  Gear ratio 35:1
    rpm = 60000000.0 / (time*pulsesPerREV*35*220);
  }
  else {
    rpm = -1*60000000.0 / (time*pulsesPerREV*35*220);
  }
  //  Accumulates every value of RPM into an array
  movingAvg[index] = rpm;
  //  Increases array's index
  index++;
  //  If the index is higher than 10, it reinitiates to 0 for moving average
  if (index >= 10) {
    index = 0;
  }  
 //  Saves this time for future iterations
  previousTime = currentTime;
}

std_msgs::Float32 output;
// Defines publisher for velocity output
ros::Publisher pub("motor_output", &output);

void setup() {
  // put your setup code here, to run once:
  lcd.init();                    
  lcd.backlight();
  pinMode(pwm, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  // Encoder Pin setup, interrupt Pin must be Pull Up
  pinMode(encoderInterrupt, INPUT_PULLUP);
  pinMode(encoderDirection, INPUT);
  // When pin goes from LOW to HIGH, it enters interruption
  attachInterrupt(digitalPinToInterrupt(encoderInterrupt), motor_pulse, RISING);
  // Initializes ROS node
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
}

void loop() {
  // Record the time
  long currT = millis();
  long time = currT - prevT;
  
  rpm = 0;
  // Reassigns RPM value with moving average filter
  for (int i = 0; i < 10; i++){
    rpm += movingAvg[i];
  }
  rpm = rpm/10;
  // Prints information on LCD Display
  output.data = rpm;
  nh.spinOnce();
  pub.publish(&output);
  if (time > 250){
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("RPM: "); 
    lcd.print(rpm*220);
    lcd.setCursor(0, 1);
    lcd.print("Rad/s: "); 
    lcd.print(rpm*220*rpm_to_radians);
    prevT = currT;
  }
}
