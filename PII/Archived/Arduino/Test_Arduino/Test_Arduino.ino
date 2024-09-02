#define IN1_PIN 3
#define IN2_PIN 4 
#define IN3_PIN 5
#define IN4_PIN 6
#define IN_1 7
#define IN_2 8
#define IN_3 9
#define IN_4 10
#define maxSpeed 1500
#define minSpeed 70

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
  stop();
}

void stop() {
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, LOW);
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
}

void startEngine() {
  digitalWrite(IN_1, HIGH);
  digitalWrite(IN_2, LOW);
  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, HIGH); 
}

void forward() {
  digitalWrite(IN1_PIN, maxSpeed); 
  analogWrite(IN2_PIN,LOW ); 
  digitalWrite(IN3_PIN, LOW); 
  analogWrite(IN4_PIN, maxSpeed);
}

void backward() {
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, HIGH); 
  digitalWrite(IN3_PIN, HIGH); 
  digitalWrite(IN4_PIN, LOW); 
}

void rotateLeft() {
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, HIGH); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, HIGH); 
}

void rotateRight() {
  digitalWrite(IN1_PIN, HIGH); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, HIGH); 
  digitalWrite(IN4_PIN, LOW); 
}

void turnLeft() {
  digitalWrite(IN1_PIN, LOW); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, HIGH); 
}

void turnRight() {
  digitalWrite(IN1_PIN, HIGH); 
  digitalWrite(IN2_PIN, LOW); 
  digitalWrite(IN3_PIN, LOW); 
  digitalWrite(IN4_PIN, LOW); 
}

void loop() {
  rotateLeft();
  }
