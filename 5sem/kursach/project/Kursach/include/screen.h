#pragma once
#include<Arduino.h>
#include <TM1637Display.h>
#include<settings.h>

class Screen
{
    // letters
#define DE (uint8_t)(0b01111001)
#define DR (uint8_t)(0b01010000)
#define DF (uint8_t)(0b01010000)
#define DI (uint8_t)(0b01010000)

    // digits
#define D0 (uint8_t)(0b00111111)
#define D1 (uint8_t)(0b00000110)
#define D2 (uint8_t)(0b01011011)
#define D3 (uint8_t)(0b01001111)

    // labels
    const uint8_t error0[4] = {DE, DR, DR, D0};
    const uint8_t error1[4] = {DE, DR, DR, D1};
    const uint8_t error2[4] = {DE, DR, DR, D2};
    const uint8_t error3[4] = {DE, DR, DR, D3};
    const uint8_t fire[4] = {DF, DI, DR, DE};

    TM1637Display display = TM1637Display(CLK, DIO);

public:
    Screen()
    {
        display.setBrightness(7);
        display.clear();
    }

    void clear()
    {
        display.clear();
    }

    void show(int value, bool leadinZero = false)
    {
        display.showNumberDec(value, leadinZero);
    }

    void showFire()
    {
        display.setSegments(fire);
    }

    void showError(uint8_t code)
    {
        switch (code)
        {
        case 0:
            display.setSegments(error0);
            break;
        case 1:
            display.setSegments(error1);
            break;
        case 2:
            display.setSegments(error2);
            break;
        default:
            display.setSegments(error3);
            break;
        }
    }
};
