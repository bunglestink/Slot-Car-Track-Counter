#include <stdio.h>

#define TRIG_PIN_1 2
#define ECHO_PIN_1 3
#define TRIG_PIN_2 4
#define ECHO_PIN_2 5


long getDurationFromSensor(int trigPin, int echoPin);


void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(TRIG_PIN_2, OUTPUT);
  pinMode(ECHO_PIN_2, INPUT);  
}


void loop() {
  static long durationTrack1, durationTrack2;
  static char serialMessage[50];

  durationTrack1 = getDurationFromSensor(TRIG_PIN_1, ECHO_PIN_1);
  //durationTrack2 = getDurationFromSensor(TRIG_PIN_1, ECHO_PIN_1);

  sprintf(serialMessage, "[{\"track\":1,\"value\":%i}]", durationTrack1);
  //sprintf(serialMessage, "[{\"track\":2,\"value\":%i}]", durationTrack2);
  Serial.println(serialMessage);

  delay(30);
}


long getDurationFromSensor(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);
  return pulseIn(echoPin, HIGH);  
}

