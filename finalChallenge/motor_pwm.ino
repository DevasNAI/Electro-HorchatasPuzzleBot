#include <ros.h>
#include <std_msgs/Float32.h>
#include  <Wire.h>
#include  <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2); 

ros::NodeHandle nh;
int pwm = 2;
int in1 = 3;
int in2 = 4;

int encoderInterrupt = 19;
int encoderDirection = 18;
volatile long pulsecount = 0;

volatile bool direction = false;

int pulsesPerREV = 12;

// Counters for  during interval
long previousTime = 0;
 
// Variable for RPM measuerment
float rpm = 0;
 
// Variable for angular velocity measurement
float ang_velocity = 0;
float ang_velocity_deg = 0;
 
const float rpm_to_radians = 0.10471975512;
const float rad_to_deg = 57.29578;

float movingAvg[10];
int index = 0;
float avg = 0.0;

long prevT = 0;

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

ros::Subscriber<std_msgs::Float32> sub("/motor_input", &messageCb);

void motor_pulse(){
  long currentTime = micros();
  long time = currentTime - previousTime;

  int val = digitalRead(encoderDirection);
  if(val == LOW) {
    //Forward
    direction = true;
  }
  else {
    //Reverse
    direction = false;
  }


  if (direction) {
    rpm = 60000000.0 / (time*pulsesPerREV*35*220);
  }
  else {
    rpm = -1*60000000.0 / (time*pulsesPerREV*35*220);
  }
  movingAvg[index] = rpm;
  index++;
  if (index >= 10) {
    index = 0;
  }  
  previousTime = currentTime;
}

std_msgs::Float32 output;
ros::Publisher pub("motor_output", &output);

void setup() {
  // put your setup code here, to run once:
  lcd.init();                    
  lcd.backlight();
  pinMode(pwm, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(encoderInterrupt, INPUT_PULLUP);
  pinMode(encoderDirection, INPUT);
  attachInterrupt(digitalPinToInterrupt(encoderInterrupt), motor_pulse, RISING);
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Record the time
  long currT = millis();
  long time = currT - prevT;

  rpm = 0;
  for (int i = 0; i < 10; i++){
    rpm += movingAvg[i];
  }
  rpm = rpm/10;
  
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
