
#define IN1_PIN 3
#define IN2_PIN 4 
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
#define maxSpeed 1023
#define minSpeed 123
#define speed 500
#define engine_speed 123
#define fb_time 0.2
#define rotate_time 0.2
#define turn_time 0.2

void setup() {
  Serial.begin(9600);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);
}
void stop(){
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, LOW);
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
}
void startEngine(float second){
  constrain(engine_speed, minSpeed, maxSpeed);
  digitalWrite(IN_1, engine_speed);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, engine_speed);
  delay(second*1000); 
}
void forward( float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, speed); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, speed);
  delay(second*1000);
  stop();
}
void backward( float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, speed); 
  digitalWrite(IN3_PIN, speed); 
  digitalWrite(IN4_PIN, LOW); 
  delay(second*1000);
  stop();
}
void rotateLeft( float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, speed); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, speed); 
  digitalWrite(IN4_PIN, LOW); 
  delay(second*1000);
  stop();
}
void rotateRight( float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, speed); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, speed); 
  delay(second*1000);
  stop();
}
void turnLeft(float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, speed); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, LOW); 
  delay(second*1000);
  stop();
}
void turnRight(float second){
  constrain(speed, minSpeed, maxSpeed);
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, speed); 
  delay(second*1000);
  stop();
}
void turnForward( int speed1, int speed2,  float second){
  constrain(speed1, minSpeed, maxSpeed);
  analogWrite(IN1_PIN, speed1);
  digitalWrite(IN2_PIN, LOW);
  constrain(speed2, minSpeed, maxSpeed);
  analogWrite(IN4_PIN, speed2);
  digitalWrite(IN3_PIN, LOW);
  delay(second*1000);
  stop();
}
void stopForever(){
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, LOW);
  while (0==0){
  delay(1000);}
}

void loop(){
  startEngine(30000);
  while (Serial.available()){
     char key = Serial.read();
     if (key == '8'){
       forward(fb_time);}
     if (key == '2' ){
       backward(fb_time);}
     if (key == '4'){
       rotateLeft(rotate_time);}
     if (key == '6'){
       rotateRight(rotate_time);}
     if (key == '5'){
       forward(fb_time*2);}
     if (key == '7'){
       turnLeft(turn_time);}
     if (key == '9'){
       turnRight(turn_time);}
    }}