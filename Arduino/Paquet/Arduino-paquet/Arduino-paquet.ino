//Ici la lecture depuis le µc se fait par "paquets" de 300 impulsions
volatile long high,low,count;
volatile long data[301];

void setup()
{
    Serial.begin(115200);
    Serial.println("start");
    high = 0;
    low = 0;
    //pinMode(3,OUTPUT);
    //digitalWrite(3,HIGH); // Pull-up


    // on déclare les interrupts
    attachInterrupt(0, interrupt_high, FALLING); //Interrupt sur D2
    attachInterrupt(1, interrupt_low, RISING); //Interrupt sur D3
}

void loop()
{
  if (count > 300)
  {
    noInterrupts();
    for (int i=0;i< 300;i++)
    {
      Serial.println(data[i]);
    }
    count = 0;
    high=micros();
    low=high;
    interrupts();
  }
}

void interrupt_high()
{
    high=micros();
    if(count == 0)
    {
      data[0] = 0;
      count ++;
    }
    if (count <= 300)
    {
      data[count] =  high-low;
      count ++;
    }
}

void interrupt_low()
{
    low = micros();
    if(count == 0)
    {
      data[0] = 1;
      count ++;
    }
    if(count <= 300)
    {
      data[count] = low-high;
      count ++;
    }

}
