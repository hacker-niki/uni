#include <Arduino.h>
#include <TM1637Display.h>

const int numSensors = 5;
const int sensorPins[numSensors] = {A0, A1, A2, A3, A4};
const int ledPin = 2;       // Пин для светодиода засветки
const int alertLedPin = 3;  // Пин для светодиода сигнализации
const int threshold = 100;   // Увеличенный порог для скачка, чтобы уменьшить ложные срабатывания
const int maxValue = 850;   // Корректное значение для засветки датчика при пламени
const int minValue = 1;     // Минимальное значение для отключенного датчика
const int numReadings = 30; // Количество чтений для усреднения фона
const int sensivity = 600;  // Чувствительность для снижения уровня опасности


#define CLK 9
#define DIO 10


int readings[numSensors][numReadings];
int indices[numSensors] = {0};
int totals[numSensors] = {0};
int averages[numSensors] = {0};
int baselines[numSensors] = {0};
bool spikeDetected[numSensors] = {false};
unsigned long overexposureStartTime = 0;
bool overexposureStarted = false;
bool alertTriggered = false; // Флаг для сигнализации

TM1637Display display = TM1637Display(CLK, DIO);


int spikeCount = 0;
int collapseCount = 0;

int cnt = 0;

void setup() {
    Serial.begin(9600);
    for (int i = 0; i < numSensors; i++) {
        for (int j = 0; j < numReadings; j++) {
            readings[i][j] = analogRead(sensorPins[i]);
            totals[i] += readings[i][j];
        }
        baselines[i] = totals[i] / numReadings;
    }
    display.clear();
    display.setBrightness(7);
}

void loop() {
    bool anyOverexposed = false;

    for (int i = 0; i < numSensors; i++) {
        totals[i] -= readings[i][indices[i]];
        readings[i][indices[i]] = analogRead(sensorPins[i]);
        totals[i] += readings[i][indices[i]];
        indices[i] = (indices[i] + 1) % numReadings;

        averages[i] = totals[i] / numReadings;
        baselines[i] = (baselines[i] * 0.9) + (averages[i] * 0.1);  // Плавная адаптация базовой линии


        Serial.print(i);
        Serial.print(":");
        Serial.println(readings[i][indices[i]]);

        // Обнаружение скачка
        if (!spikeDetected[i] && abs(readings[i][indices[i]] - baselines[i]) > threshold) {
            spikeDetected[i] = true;
            Serial.print("Датчик ");
            Serial.print(i);
            Serial.println(": Скачок обнаружен!");
            spikeCount++;
        }

        // Сброс скачка, если сигнал вернулся в норму
        if (spikeDetected[i] && abs(readings[i][indices[i]] - baselines[i]) < threshold) {
            spikeDetected[i] = false;
            Serial.print("Датчик ");
            Serial.print(i);
            Serial.println(": Падение после скачка!");
        }

        // Обнаружение засветки
        if (readings[i][indices[i]] > maxValue) {
            Serial.print("Датчик ");
            Serial.print(i);
            Serial.println(": Засвечен!");
            anyOverexposed = true;  // Засветка обнаружена
        }

        // // Обнаружение отключения датчика
        // if (readings[i][indices[i]] < minValue) {
        //     Serial.print("Датчик ");
        //     Serial.print(i);
        //     Serial.println(": Закрыт!");
        // }
    }

    // Обработка засветки
    if (anyOverexposed) {
        if (!overexposureStarted) {
            overexposureStartTime = millis();
            overexposureStarted = true;
        }
        if (millis() - overexposureStartTime >= 5000) { // 5 секунд ожидания для подтверждения
            digitalWrite(ledPin, HIGH);  // Включение светодиода через 5 секунд засветки
        }
    } else {
        overexposureStarted = false;
        digitalWrite(ledPin, LOW);  // Выключение светодиода
    }

    // Сигнализация при множественных скачках
    if (spikeCount > 3) {  // Количество скачков для срабатывания сигнализации
        alertTriggered = true;  // Установка флага сигнализации
    }

    if (alertTriggered) {
        display.showNumberDec(9999);
    }else{
        int out =0;
        for(int i =0; i < numSensors; i++){
            out+=readings[i][numReadings-1];
        }
        out/=numSensors;
        display.showNumberDec(out, true);
    }

    // Понижение уровня опасности
    if (cnt++ > sensivity) {
        cnt = 0;  // Сброс счётчика
        if (spikeCount > 0) spikeCount--;  // Плавное снижение счётчика скачков
    }

    delay(2);  // Небольшая задержка для стабилизации
}