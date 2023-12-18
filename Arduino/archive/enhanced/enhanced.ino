#define IN1_PIN 3
#define IN2_PIN 4
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
const int maxSpeed = 255;
const int normSpeed = 100;
const int turnSpeed = 50;



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

void stop(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
}

void startEngine(){
  digitalWrite(IN_1, HIGH);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3,LOW);
  digitalWrite(IN_4, HIGH);
}

void waitUntilRelease(){
    while (true){
    if (Serial.available()){
        String msg = Serial.readStringUntil("\n");
        if (msg == "stop"){
            break;
        }
    }
  }
  stop();
}

void sendDoneSignal(){
  Serial.println("stop");
}

void forward(){
  startEngine();
  analogWrite(IN1_PIN, normSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, normSpeed);
  waitUntilRelease();
}

void backward(){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, normSpeed);
  analogWrite(IN3_PIN, normSpeed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void rotateLeft(){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, turnSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  waitUntilRelease();
}
void rotateRight(){
  startEngine();
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, turnSpeed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void turnLeft(){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  waitUntilRelease();
}

void turnRight(){
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void forward(float second){
  startEngine();
  analogWrite(IN1_PIN, normSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, normSpeed);
  delay(second*1000);
  Serial.println("Done executing");
}

void backward(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, normSpeed);
  analogWrite(IN3_PIN, normSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  Serial.println("Done executing");
}

void rotateLeft(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, turnSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}
void rotateRight(float second){
  startEngine();
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, turnSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void turnLeft(float second){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, turnSpeed);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void turnRight(float second){
  analogWrite(IN1_PIN, turnSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  stop();
  Serial.println("Done executing");
}

void caseChoose(){
  if (Serial.available()){
    String msg = Serial.readStringUntil("\n");
    msg.trim();
    //stop control in python
    if (msg == "forward"){
      sendDoneSignal();
      forward();
    }
    else if (msg == "backward"){
      sendDoneSignal();
      backward();
    }
    else if (msg == "rotateRight"){
      sendDoneSignal();
      rotateRight();
    }
    else if (msg == "rotateLeft"){
      sendDoneSignal();
      rotateLeft();
    }
    else if (msg == "turnLeft"){
      sendDoneSignal();
      turnLeft();
    }
    else if (msg == "turnRight"){
      sendDoneSignal();
      turnRight();
    }
    else if (msg == "farLeft"){
      sendDoneSignal();
      turnLeft(0.5);
    }


  }
}

void loop() {
   startEngine();
   
  else{
    stop(0.1);
  }
}