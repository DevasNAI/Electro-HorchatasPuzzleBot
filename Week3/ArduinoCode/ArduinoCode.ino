//Incluir las librearias necesarias
#include <ros.h> //Libreria para usar los comandos de ROS
#include <std_msgs/Float32.h> //Libreria para utilizar datos de tipo Float32

ros::NodeHandle nh; //Este comando inicializa el nodo 

// Definimos los pines del Arduino y los guardamos en las variables
int enable = 2; //En el pin 2 mandamos el valor PWM
//Estos pines definen si el motor ira en el sentido horario o al contrario
int in1 = 3; //Si mandamos HIGH ira en sentido horario
int in2 = 4; //Si mandamos High ira en sentido anti-horario

// Definimos la variable PWM donde estaremos almacenando el dato recibido del nodo de ROS
float PWM = 0;

// En esta funcion recibimos el dato del nodo de ROS y calculamos como se debera de mover el motor
void message( const std_msgs::Float32& PWM1){ //Recibimos el topico en la variable PWM1
  PWM = PWM1.data; //Almacenamos el topico en la variable PWM
  // Definimos como iniciara normalmente el codigo
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);
  if (PWM > 255){  //Si el valor de PWM es mayor a 255 (El max permitido) unicamente mandamos 255 al motor
    analogWrite(enable, 255);
  }
  else if (PWM<=0){  // Si PWM es menor o igual a 0 invertimos el movimiento del motor
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enable, -1*PWM1.data); // Como PWM es negativo y no podemos mandar valores negativos lo multiplicamos por -1
  }
  else if (PWM>0 and PWM<255){ //Si PWM es mayor a 0 y menor a 255 funciona con normalidad
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enable, PWM1.data);
  }
  else if (PWM<-255){  // Si PWM es menor a -255 invertimos el movimiento y mandamos 255 constante
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enable, 255);
    
  }
}

// Con esto nos suscribimos al topico de ROS y mandamos el dato a la funcion message
ros::Subscriber<std_msgs::Float32> sub("/set_point", &message);

// Aqui se inicializa y define el codigo
void setup() {
  // put your setup code here, to run once:
  pinMode(enable, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  // Inicializamos el nodo y el subscribe
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
