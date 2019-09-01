int output;
char lastFlag = 0;
const int pin = 6;
//const int button = 2;
//int buttonStatus = 0;
int led1 = 7;
int led2 = 8;
int led3 = 9;
void setup()
{
  Serial.begin(9600);
  //pinMode(button,INPUT);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
}

void loop()
{
  //buttonStatus = digitalRead(button);
  
  //if(buttonStatus==HIGH){
     output = map(analogRead(A0), 0, 1023, 0, 255);
     if (Serial.available() > 0) {
      Serial.println(output, DEC);
     }
     char flag = lastFlag;
     if (Serial.available() > 0) {
        flag = Serial.read();
     }
     
     if(flag == '1'){
      lastFlag = '1';
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      digitalWrite(led3, HIGH);
      analogWrite(pin, output);
     }
     else if(flag == '2'){
      lastFlag = '2';
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
      digitalWrite(led3, LOW);
      analogWrite(pin, output);
     }
     else if(flag == '3'){
      lastFlag = '3';
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
      digitalWrite(led3, LOW);
      analogWrite(pin, output);
     }
  //}
}
