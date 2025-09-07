#pragma once
#include<screen.h>
#include<sensor.h>

class Detector
{
public:
    Screen screen;

    Sensor sensors[sensorsCount];

    bool fire = false;

    int error = -1;

    Detector()
    {
    }

    void updateReadings()
    {
        for (int i = 0; i < sensorsCount; i++)
        {
            int reading = analogRead(sensorPins[i]);

            sensors[i].updateReading(reading);
        }
    }

    int getAverage()
    {
        int average = 0;
        for (int i = 0; i < sensorsCount; i++)
        {
            average += sensors[i].getMid();
        }
        return average / sensorsCount;
    }

    void checkForSpikes()
    {
        int average = getAverage();

        for (int i = 0; i < sensorsCount; i++)
        {
            if (sensors[i].isTooBright())
            {
                error = 2;
            }
            int spike = sensors[i].spikeCount(average);
            Serial.println(spike);
            if (spike > 0)
            {
                fire = true;
            }
            else if (spike == -1)
            {
                error = 3;
            }
        }
    }

    unsigned long lastBlinkTime = 0;
    bool isShowingError = false;

    void displayState(int value)
    {
        if (fire)
        {
            screen.showFire();
        }
        else
        {
            if (error > -1)
            {
                unsigned long currentTime = millis();
                if (currentTime - lastBlinkTime >= 750)
                {
                    lastBlinkTime = currentTime;
                    isShowingError = !isShowingError;
                }

                if (isShowingError)
                {
                    screen.showError(error);
                }
                else
                {
                    screen.show(value);
                }
            }
            else
            {
                screen.show(value);
            }
        }
    }

    void tick()
    {
        updateReadings();

        checkForSpikes();

        displayState(getAverage());

        delay(delayMillisec); // Небольшая задержка для стабилизации
    }
};
