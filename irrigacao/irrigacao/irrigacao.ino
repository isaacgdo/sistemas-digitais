int output;
int lastFlag = 0;
String inString = "";
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
  
   output = map(analogRead(A0), 0, 1023, 0, 255);
   if (Serial.available() > 0) {
    Serial.println(output, DEC);
   }
   int flag = lastFlag;

   if (Serial.available() > 0) {
     while (Serial.available() > 0) {
        int inChar = Serial.read();
        if (isDigit(inChar)) {
          // convert the incoming byte to a char and add it to the string:
          inString += (char)inChar;
        }
     }

     flag = inString.toInt();
   }

   if (flag == 1){
     lastFlag = 1;
     inString = "";
     digitalWrite(led1, LOW);
     digitalWrite(led2, LOW);
     digitalWrite(led3, HIGH);
     analogWrite(pin, output);
   }
   else if (flag == 2){
     lastFlag = 2;
     inString = "";
     digitalWrite(led1, LOW);
     digitalWrite(led2, HIGH);
     digitalWrite(led3, LOW);
     analogWrite(pin, output);
   }
   else if (flag == 3){
     lastFlag = 3;
     inString = "";
     digitalWrite(led1, HIGH);
     digitalWrite(led2, LOW);
     digitalWrite(led3, LOW);
     analogWrite(pin, output);
   }
   else if (flag > 3){
     inString = "";
     digitalWrite(led1, LOW);
     digitalWrite(led2, LOW);
     digitalWrite(led3, LOW);
     analogWrite(pin, 0);
     delay(flag*1000);
   }
}
