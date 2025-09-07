#pragma once
#include<queue.h>
#include<settings.h>

class Sensor
{
public:
    Queue<int> readings = Queue<int>(readingsCount);
    const int spikeReadings = allowedSpikeDelay / delayMillisec;


    int getMid()
    {
        int mid = 0;
        for (int i : readings)
        {
            mid += i;
        }
        return mid / readings.count();
    }

    int getMax()
    {
        int maximum = 0;
        for (int i : readings)
        {
            maximum = max(i, maximum);
        }
        return maximum;
    }

    int spikeCount(int average)
    {
        int spikeCount = 0;
        int currentSpike = 0;
        int lastSpikeTime = 0;
        int currentTime = 0;

        for (int i : readings)
        {
            currentTime += delayMillisec;
            if (i - average >= allowedSpikeThreshold)
            {
                currentSpike += 1;
                if (currentSpike >= spikeReadings)
                {
                    spikeCount++;
                    currentSpike = 0;
                    lastSpikeTime = currentTime;
                }
            }
            else
            {
                currentSpike = 0;
            }
        }

        // Check if spikes are too close
        if (spikeCount > 1)
        {
            int timeBetweenSpikes = currentTime - lastSpikeTime;
            if (timeBetweenSpikes < allowedSpikeDelay)
            {
                spikeCount = -1; // error
            }
        }

        return spikeCount;
    }

    void updateReading(int value)
    {
        readings.push(value);
    }

    bool isTooBright()
    {
        return this->getMax() > maximumValueAllowed;
    }
};

