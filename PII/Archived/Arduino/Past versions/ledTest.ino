void setup() {  
   pinMode(2, OUTPUT);
   Serial.begin(9600);
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
  digitalWrite(2, LOW);
}

void blink(){
  digitalWrite(2, HIGH);
  waitUntilRelease();
}

void loop() {
   if (Serial.available()){
    char msg = Serial.read();
    if (msg == '2'){
     blink();
    }
   }
}