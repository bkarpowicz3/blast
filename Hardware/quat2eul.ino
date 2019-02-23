/*Attempt to convert quaternions to euler angles
 */
#include <math.h>
#include <Arduino.h>
#include <stdio.h>

float *eulerangles;

void setup() {
  Serial.begin(115200);
}

void loop() {
   eulerangles = quat2eul(0.6259, 0.7761, 0.07608, 0); 
}

float * quat2eul(float q0, float q1, float q2, float q3) {

  float roll = degrees(atan2((2*(q0*q1+q2*q3)),(1-2*(square(q1)+square(q2))))); //arctan2 = arc tangent of y/x
  float pitch = degrees(asin(2*(q0*q2-q3*q1)));
  float yaw = degrees(atan2((2*(q0*q3+q1*q2)),(1-2*(square(q2)+square(q3)))));
  float euler[3] = {roll, pitch, yaw};
  
  for (int i =0; i<3;++i ){
   Serial.print(euler[i]);
   Serial.print('\t');
  }
  Serial.println();
  return euler;
}
