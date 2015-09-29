char* carte[114] = {"h 480", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 480", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 480", "l 480", "h 480", "l 480", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 480", "l 240", "h 240", "l 480", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 480", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 480", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 240", "l 240", "h 480", "l 240", "h 240", "l 480", "h 240", "l 240", "h 480", "l 240", "h 240", "l 240", "h 240", "l 480"};

void setup()
{
    Serial.begin(115200);
    Serial.println("hello world!");
    high = 0;
    low = 0;
    //pinMode(3,OUTPUT);
    //digitalWrite(3,HIGH); // Pull-up
    //attachInterrupt(0, interrupt_high, FALLING); //Interrupt sur D2
    //attachInterrupt(1, interrupt_low, RISING); //Interrupt sur D3
}

void loop()
{
  for(int i=0;i<114;i++)
  {
    Serial.println(carte[i]);
    delayMicroseconds(200);
  }
}
