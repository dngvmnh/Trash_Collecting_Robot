#define IN1_PIN 3
#define IN2_PIN 4
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
#define maxSpeed 500
#define speed 150


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
  digitalWrite(IN_1, LOW);
  analogWrite(IN_2, LOW);
  analogWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
}

void waitUntilRelease(){
    while (true){
    if (Serial.available()){
        char msg = Serial.read();
        if (msg == '0'){
            break;
        }
    }
  }
  stop();
}

void forward(){
  startEngine();
  analogWrite(IN1_PIN, speed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, speed);
  waitUntilRelease();
}

void backward(){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, speed);
  analogWrite(IN3_PIN, speed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}

void rotateRight(){
  // startEngine();
  analogWrite(IN2_PIN, maxSpeed);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, maxSpeed);
  waitUntilRelease();
}
void rotateLeft(){
  startEngine();
  analogWrite(IN1_PIN, maxSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, maxSpeed);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}
void turnRight(){
  // startEngine();
  analogWrite(IN2_PIN, LOW);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, maxSpeed);
  waitUntilRelease();
}
void turnLeft(){
  startEngine();
  analogWrite(IN1_PIN, maxSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  waitUntilRelease();
}
void forward(float second){
  startEngine();
  analogWrite(IN1_PIN, maxSpeed);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, maxSpeed);
  delay(second*1000);
  waitUntilRelease();
  Serial.println("Done executing");
}

void backward(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, maxSpeed);
  analogWrite(IN3_PIN, maxSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);  
  waitUntilRelease();
  Serial.println("Done executing");
}

void rotateRight(float second){
  startEngine();
  digitalWrite(IN1_PIN, LOW);
  analogWrite(IN2_PIN, maxSpeed);
  digitalWrite(IN3_PIN, LOW);
  analogWrite(IN4_PIN, maxSpeed);
  delay(second*1000);
  waitUntilRelease();
  Serial.println("Done executing");
}
void rotateLeft(float second){
  startEngine();
  analogWrite(IN1_PIN, maxSpeed);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(IN3_PIN, maxSpeed);
  digitalWrite(IN4_PIN, LOW);
  delay(second*1000);
  waitUntilRelease();
  Serial.println("Done executing");
}


void loop(){
  if (Serial.available()>0){
  String command = Serial.readStringUntil('\n');
  command.trim();
  if(command == "turnLeft"){
    Serial.println("Lefted");
    turnLeft();
  }
  if(command == "turnRight"){
    Serial.println("Righted");
    turnRight();
  }
  if(command == "forward"){
    forward();
    Serial.println("Fowarded");
  }
  if(command == "backward"){
    backward();
    Serial.println("Backwarded");
  }
  if(command == "rotateLeft"){
    Serial.println("Lefted");
    rotateLeft();
  }
  if(command == "rotateRight"){
    Serial.println("Righted");
    rotateRight();
  }
  // if(command == "back3000"){ 
  //   backward();
  //   delay(3000)
  //   Serial.println("Backwarded");
  // }
}
}