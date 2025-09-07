#include <Arduino.h>
#include<detector.h>

Detector detector;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    detector.tick();
}
