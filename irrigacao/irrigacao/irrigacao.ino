int output;
int lastFlag = 0;
String inString = "";
const int pin = 6;
bool lastState = false;
bool fnc3 = false;
bool lowPWM = false;

int led1 = 7;
int led3 = 9;

void setup()
{
  Serial.begin(9600);
  pinMode(led1,OUTPUT);
  pinMode(led3,OUTPUT);
  pinMode(pin,OUTPUT);
}

bool swapState()
{
  bool temp = false;
  if(lastState == false) {
    temp = true;
  }
  
  lastState = temp;
  return temp;
}

void loop()
{
   output = map(analogRead(A0), 0, 1023, 0, 255);
   if (Serial.available() > 0) {
     if (lowPWM == false) {
       Serial.println(output, DEC);
     } else {
       Serial.println(0, DEC);
     }
   }
   int flag = lastFlag;

   if (Serial.available() > 0) {
     while (Serial.available() > 0) {
        int inChar = Serial.read();
        if (isDigit(inChar)) {
          inString += (char)inChar;
        }
     }

     flag = inString.toInt();
   }

   if (flag == 3) {
     fnc3 = true;
   }

   if (flag == 1 && fnc3 == false){
     lastFlag = 1;
     inString = "";
     digitalWrite(led1, LOW);
     digitalWrite(led3, HIGH);
     analogWrite(pin, output);
     output = map(analogRead(A0), 0, 1023, 0, 255);
     lowPWM == false;
   }
   else if (flag == 2){
     lastFlag = 2;
     inString = "";
     digitalWrite(led1, HIGH);
     digitalWrite(led3, LOW);
     analogWrite(pin, 0);
     fnc3 = false;
   }
   else if (flag == 3 && fnc3 == true){
     fnc3 = true;
     inString = "";
     if(swapState() == true) {
       digitalWrite(led1, HIGH);
       digitalWrite(led3, LOW);
       analogWrite(pin, 0);
       lowPWM = true;
     } else {
       analogWrite(pin, output);
       digitalWrite(led1, LOW);
       digitalWrite(led3, HIGH);
       lowPWM = false;
     }
     lastFlag = 0;
   }
}
