#include <FastBot.h>
#include <ESP8266WebServer.h>
#include <ESPAsyncTCP.h>
#include <ESP8266WiFi.h>

#define WIFI_SSID "Gachi-club"
#define WIFI_PASS "ksisisshit"
#define AP_SSID "esp8266"
#define AP_PASS "password"
#define BOT_TOKEN "6597049665:AAFkidl30bcbSROQ8ffCm6E4ZBv1X4DQvXI"
#define SENSOR_PIN 5   //D1
#define RELE_PIN 4     //D2
#define BUTTON_PIN 12  //D6

#define PIN_TONE 13  // D7 пин для пищалки

String userId = "";
String WiFi_Ssid = "";
String WiFi_Pass = "";
bool set = true;
bool alarm = false;

unsigned long timerPisk = 0;
bool fPisk = 0;
FastBot bot(BOT_TOKEN);
ESP8266WebServer server(80);

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WiFi_Ssid, WiFi_Pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected");
  bot.sendMessage("Fuck off pieace of meat", userId);
}

void setupWithHotspot() {
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS);
  Serial.println(WiFi.softAPIP().toString());
}

// обработчик сообщений
void newMsg(FB_msg& msg) {
  // выводим всю информацию о сообщении
  Serial.println(msg.toString());

  // отправить сообщение обратно
  bot.sendMessage(msg.text, msg.chatID);
}

void handleRootPath() {
  String page;
  if (server.method() == HTTP_POST) {
    Serial.println("received");
    // Обработка POST-запроса
    userId = server.arg("userId");
    WiFi_Ssid = server.arg("WiFi_Ssid");
    WiFi_Pass = server.arg("WiFi_Pass");
    page = "<!DOCTYPE html>\n"
           "<html>\n"
           "<head>\n"
           "  <title>Request Received</title>\n"
           "</head>\n"
           "<body>\n"
           "  <h2>Request Received</h2>\n"
           "  <p>Your request has been received.</p>\n"
           "</body>\n"
           "</html>";
    set = false;
    server.send(200, "text/html", page);
    Serial.println(userId);

    server.stop();
  } else {
    Serial.println("send");
    page = "<!DOCTYPE html>\n"
           "<html>\n"
           "<head>\n"
           "  <title>Настройка</title>\n"
           "  <style>\n"
           "    body {\n"
           "      font-family: Arial, sans-serif;\n"
           "      margin: 20px;\n"
           "    }\n"
           "    h2 {\n"
           "      color: #333;\n"
           "    }\n"
           "    form {\n"
           "      width: 400px;\n"
           "    }\n"
           "    label {\n"
           "      display: block;\n"
           "      margin-bottom: 5px;\n"
           "      color: #555;\n"
           "    }\n"
           "    input[type=\"text\"],\n"
           "    input[type=\"password\"] {\n"
           "      width: 100%;\n"
           "      padding: 8px;\n"
           "      border: 1px solid #ccc;\n"
           "      border-radius: 4px;\n"
           "    }\n"
           "    textarea {\n"
           "      width: 100%;\n"
           "      height: 100px;\n"
           "      padding: 8px;\n"
           "      border: 1px solid #ccc;\n"
           "      border-radius: 4px;\n"
           "      resize: vertical;\n"
           "    }\n"
           "    input[type=\"submit\"] {\n"
           "      background-color: #4CAF50;\n"
           "      color: white;\n"
           "      padding: 10px 20px;\n"
           "      border: none;\n"
           "      border-radius: 4px;\n"
           "      cursor: pointer;\n"
           "    }\n"
           "    input[type=\"submit\"]:hover {\n"
           "      background-color: #45a049;\n"
           "    }\n"
           "  </style>\n"
           "</head>\n"
           "<body>\n"
           "  <h2>Настройка esp3286</h2>\n"
           "  <form action=\"/\" method=\"post\">\n"
           "    <label for=\"userId\">User ID:</label>\n"
           "    <input type=\"text\" id=\"userId\" name=\"userId\">\n"
           "    <label for=\"WiFi_Ssid\">WiFi SSID:</label>\n"
           "    <input type=\"text\" id=\"WiFi_Ssid\" name=\"WiFi_Ssid\">\n"
           "    <label for=\"WiFi_Pass\">WiFi Password:</label>\n"
           "    <input type=\"password\" id=\"WiFi_Pass\" name=\"WiFi_Pass\">\n"
           "    <input type=\"submit\" value=\"Submit\">\n"
           "  </form>\n"
           "</body>\n"
           "</html>";
    server.send(200, "text/html", page);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println();

  setupWithHotspot();
  server.on("/", handleRootPath);
  server.begin();
  pinMode(SENSOR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(RELE_PIN, OUTPUT);
}

void loop() {
  if (set) {
    server.handleClient();
  } else {
    if (digitalRead(SENSOR_PIN) == 0 && !alarm) {
      Serial.println("ALRARM");
      alarm = true;
      bot.sendMessage("ALARM!!!", userId);
    }
    if (alarm) {
      digitalWrite(RELE_PIN, HIGH);
      if(millis() - 500 >= timerPisk){
        if(fPisk){
          tone(PIN_TONE, 1000);
          fPisk = !fPisk;
        } else {
         noTone(PIN_TONE);
         fPisk = !fPisk;
        }
        timerPisk = millis();
      }
    } else {
      digitalWrite(RELE_PIN, LOW);
      noTone(PIN_TONE);
    }
    if (digitalRead(BUTTON_PIN) == 1) {
      Serial.println("RESETTED");
      alarm = false;
      bot.sendMessage("RESETTED", userId);
    }

    if (!alarm) {
      if (WiFi.status() == WL_CONNECTED) {
      } else {
        connectWiFi();
        Serial.println("WiFi Disconnected!!!");
        Serial.println("Trying to establish the connection...");

        while (WiFi.status() != WL_CONNECTED) {
          delay(1000);
          Serial.print(".");
        }

        Serial.println("");
        Serial.print("WiFi Connected with IP Address: ");
        Serial.println(WiFi.localIP());
      }
    }
  }
}
