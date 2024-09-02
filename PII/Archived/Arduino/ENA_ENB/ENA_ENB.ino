int enA = 11;
int in1 = 3;
int in2 = 4; 
int in3 = 5; 
int in4 = 6; 
int enB = 12;  
int i=150;
 
void setup()
{
    pinMode(enA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT); 
    pinMode(enB,OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);
}
 
void forward()
{
    // for(i=0;i<=255;i++){
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
        analogWrite(enB, i); 
        analogWrite(enA, i); 
        delay(100);
    
    // for(i=255;i>=0;i--){
    //     digitalWrite(in1, HIGH);
    //     digitalWrite(in2, LOW);
    //     digitalWrite(in3, LOW);
    //     digitalWrite(in4, HIGH);
    //     analogWrite(enB, i); 
    //     analogWrite(enA, i); 
    //     delay(100);}
} 

void loop() {
  // forward();
}
