#include <stdio.h>

#define ECHO_PIN_1 7
#define TRIG_PIN_1 8
#define LED_PIN 13

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  static long duration, distance;
  static char serialMessage[50];
  
  // TODO: expand this to add a second track.
  digitalWrite(TRIG_PIN_1, LOW);
  delayMicroseconds(2);
  
  digitalWrite(TRIG_PIN_1, HIGH);
  delayMicroseconds(10);
  
  digitalWrite(TRIG_PIN_1, LOW);
  duration = pulseIn(ECHO_PIN_1, HIGH);
  
  distance = duration / 58.2;
  sprintf(serialMessage, "[{\"track\":1,\"value\":%i}]", distance);
  Serial.println(serialMessage);
  
  delay(30);
}

