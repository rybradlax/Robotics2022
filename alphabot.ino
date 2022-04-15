#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x04
int pin = 6;
int pixels = 24;
Adafruit_NeoPixel ring = Adafruit_NeoPixel(pixels, pin, NEO_GRB + NEO_KHZ800);
uint32_t green = ring.Color(0, 255, 0);
uint32_t black = ring.Color(0, 0, 0);
uint32_t purple = ring.Color(255, 0, 255);
uint32_t blue = ring.Color(0, 0, 255);
uint32_t red = ring.Color(255, 0, 0);
bool seeTarget = false;
short lightPos = 0;
short const LOW_BRIGHTNESS = 65;
short const MED_BRIGHTNESS = 100;
short const HIGH_BRIGHTNESS = 150;
short brightness = LOW_BRIGHTNESS;
long prevTime = millis();
int INTERVAL = 50;

void receiveData(int byteCount){
  while(Wire.available() > 0) {
    short num = Wire.read();
    Serial.println(num);
    short num2 =Wire.read();
    String number = "";
    for(int x = 0; x < num2; x++) 
    {
      number+=Wire.read();
    }
    switch(num) {
      case(0):
        if(number.toInt() == 1)
          seeTarget = true;
        else
          seeTarget = false;
        break;
      case(1):
        /*if(number.toInt() >= HIGH_BRIGHTNESS)
          brightness = HIGH_BRIGHTNESS;
        else if(number.toInt() >= MED_BRIGHTNESS)
          brightness = MED_BRIGHTNESS;
        else
          brightness = LOW_BRIGHTNESS;*/
        brightness = number.toInt();
        Serial.println(brightness);
        if(ring.getBrightness() != brightness)
          ring.setBrightness(brightness);
        break;
      default:
        break;
    }
  }     
}

void sendData(int number){
  Wire.write(number);
}

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Serial.begin(9600);
  ring.begin();
  for(int x=0; x<pixels; x++) {
    ring.setPixelColor(x, green);
  }
  ring.show();
  ring.setBrightness(brightness);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println(seeTarget);
  if(millis() - prevTime > INTERVAL) {
    ring.setPixelColor(lightPos, green);
    lightPos = (lightPos < 24) ? lightPos + 1 : 0; //24 -> 11
    ring.setPixelColor(lightPos, black);
    if(seeTarget)
      ring.setPixelColor(lightPos, red);
    ring.show();
    prevTime = millis();
  }
}
