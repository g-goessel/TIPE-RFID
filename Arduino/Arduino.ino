volatile unsigned long high,low;

void setup()
{
    Serial.begin(115200);
    Serial.println("hello world!");
    high = 0;
    low = 0;
    //pinMode(3,OUTPUT);
    //digitalWrite(3,HIGH); // Pull-up
    attachInterrupt(0, interrupt_high, FALLING); //Interrupt sur D2
    attachInterrupt(1, interrupt_low, RISING); //Interrupt sur D3
}

void loop()
{
}

void interrupt_high()
{
    high=micros();
    //Serial.print("h ");
    Serial.println(high-low);
}

void interrupt_low()
{
    low = micros();
    //Serial.print("l ");
    Serial.println(low-high);
}
