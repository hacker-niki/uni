#pragma once
#include<Arduino.h>

/* hardware settings */

// sensors configuration
#define sensorsCount 5
const int sensorPins[] = {A0, A1, A2, A3, A4};

// display configuration
#define CLK 9
#define DIO 10

/* hardware settings */


/* software settings */

#define readingsCount 10
#define delayMillisec 2
#define allowedSpikeDelay 40
#define allowedSpikeThreshold 60
#define maximumValueAllowed 900

/* software settings */