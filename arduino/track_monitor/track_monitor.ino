#include <stdio.h>

#define ECHO_PIN_1 7
#define TRIG_PIN_1 8
#define LED_PIN 13

long getDurationFromSensor(int trigPin, int echoPin);


void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  static long durationTrack1;
  static char serialMessage[50];

  // TODO: expand this to add a second track.
  durationTrack1 = getDurationFromSensor(TRIG_PIN_1, ECHO_PIN_1);

  sprintf(serialMessage, "[{\"track\":1,\"value\":%i}]", durationTrack1);
  Serial.println(serialMessage);

  delay(30);
}


long getDurationFromSensor(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);
  return pulseIn(ECHO_PIN_1, HIGH);  
}

