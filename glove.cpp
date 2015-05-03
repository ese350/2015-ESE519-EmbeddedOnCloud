/*
 * ESE 519 - Final Project
 * A Real time home infotainment system
 * Team Members: Aditya Deshpande, Cheng Cheng, Nishank Shinde
 * glove.cpp
*/

#include "mbed.h"
#include "PololuLedStrip.h"
#include "MRF24J40.h"
#include "L3GD20.h"
#include "LSM303DLHC.h"
#include "PulseSensor.h"
 
#define M_PI 3.14159265358979323846
#define GYRO_SENSITIVITY 286             //Max: +-286
#define SAMPLING_PERIOD 0.01              

#define HIH6130_ADDRESS7BIT 0x27
#define HIH6130_ADDRESS8BIT 0x27 << 1
#define BAUD_RATE 9600
#define I2C_FREQUENCY 400000

#define LED_COUNT 5

DigitalOut led1(LED1);

PololuLedStrip ledStrip1(p25);           //LED Strip - finger 1
PololuLedStrip ledStrip2(p24);           //LED Strip - finger 2
PololuLedStrip ledStrip3(p23);           //LED Strip - finger 3
PololuLedStrip ledStrip4(p22);           //LED Strip - finger 4

AnalogIn f1(p17);                        // Flex sensor - finger 1
AnalogIn f2(p18);                        // Flex sensor - finger 2
AnalogIn f3(p19);                        // Flex sensor - finger 3
AnalogIn f4(p20);                        // Flex sensor - finger 4
AnalogIn pulse_sensor(p16);


rgb_color colors[LED_COUNT];             // Stores the RGB color values for every strip
Timer timer_led;

//          sda  scl
L3GD20 gyro(p28, p27);
Serial pc(USBTX, USBRX);
LSM303DLHC compass(p28, p27);

int current_BPM = 0;                    // BPM for pulse sensor
          
MRF24J40 mrf(p11, p12, p13, p14, p21);  //RF transceiver

const float degToRad = M_PI/180;

float bias_ax, bias_ay, bias_az;
float bias_mx, bias_my, bias_mz;
float bias_gx, bias_gy, bias_gz;

float ax, ay, az;
float mx, my, mz;
float gx, gy, gz;

float pitch = 0, roll = 0;
float flex_sensor_read = 0.0f;
  
Timer timer;                            // To send data to the central node after regular intervals

  
// Send / receive buffers.
// IMPORTANT: The MRF24J40 is intended as zigbee tranceiver; it tends
// to reject data that doesn't have the right header. So the first 
// 8 bytes in txBuffer look like a valid header. The remaining 120
// bytes can be used for anything you like.
uint8_t txBuffer[128]= {1, 8, 0, 0xA1, 0xB2, 0xC3, 0xD4, 0x00};
uint8_t rxBuffer[128];
uint8_t rxLen;

Timer pulse_timer;

uint8_t pulse(){
    static float oldval;
    static float duration;
    static uint8_t BPM;

    float val = pulse_sensor.read();
    if (val >= 0.52 && oldval < 0.52 ){
      duration = pulse_timer.read();
      pulse_timer.reset();
      if (duration > 0.5 && duration < 1.5){
        BPM = (uint8_t)(60 / duration);        
        //pc.printf("%f %f %f\n\r ", val, duration, (60 / duration));
      }  
    }
    oldval = val;  
    return BPM;
}

void init() {
    for (int i=0; i<500; i++) {
        compass.read(&ax, &ay, &az, &mx, &my, &mz);
        gyro.read(&gx, &gy, &gz);
        bias_ax += ax; bias_ay += ay; bias_az += az;
        bias_mx += mx; bias_my += my; bias_mz += mz;
        bias_gx += gx; bias_gy += gy; bias_gz += gz;
        wait(0.05);
    }
    bias_ax = bias_ax/500; bias_ay = bias_ay/500; bias_az = bias_az/500;
    bias_mx = bias_mx/500; bias_my = bias_my/500; bias_mz = bias_mz/500;
    bias_gx = bias_gx/500; bias_gy = bias_gy/500; bias_gz = bias_gz/500;
}

void compFilter(float ax, float ay, float az, float gx, float gy) {
    float pitchAcc, rollAcc;
    
    pitch += gx/GYRO_SENSITIVITY*SAMPLING_PERIOD;
    roll -= gy/GYRO_SENSITIVITY*SAMPLING_PERIOD;
    
    int threshold = abs(ax) + abs(ay) + abs(az);
  
    if (threshold > 4096 && threshold < 32768) {     //band-pass filter
//        pc.printf("%d   ", threshold);
        rollAcc = atan(ay/az)*180/M_PI;
        pitchAcc = atan(-ax/az)*180/M_PI;
        
        pitch = pitch*0.9 + pitchAcc*0.1;     // 98% -   2%
        roll = roll*0.9 + rollAcc*0.1;
    }
}

// Converts a color from the HSV representation to RGB.
rgb_color hsvToRgb(float h, float s, float v)
{
    int i = floor(h * 6);
    float f = h * 6 - i;
    float p = v * (1 - s);
    float q = v * (1 - f * s);
    float t = v * (1 - (1 - f) * s);
    float r = 0, g = 0, b = 0;
    switch(i % 6){
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        case 5: r = v; g = p; b = q; break;
    }
    return (rgb_color){r * 255, g * 255, b * 255};
}


bool getOrientation(float* orientation) {
  // Validate input and available sensors.

  // Grab an acceleromter and magnetometer reading.
  //sensors_event_t accel_event;
  //_accel->getEvent(&accel_event);
  //sensors_event_t mag_event;
  //_mag->getEvent(&mag_event);

  compass.read(&ax, &ay, &az, &mx, &my, &mz);
  gyro.read(&gx, &gy, &gz);
        
  float const PI_F = 3.14159265F;

  // roll: Rotation around the X-axis. -180 <= roll <= 180                                          
  // a positive roll angle is defined to be a clockwise rotation about the positive X-axis          
  //                                                                                                
  //                    y                                                                           
  //      roll = atan2(---)                                                                         
  //                    z                                                                           
  //                                                                                                
  // where:  y, z are returned value from accelerometer sensor                                      
  orientation[0] = (float)atan2(ay, az);

  // pitch: Rotation around the Y-axis. -180 <= roll <= 180                                         
  // a positive pitch angle is defined to be a clockwise rotation about the positive Y-axis         
  //                                                                                                
  //                                 -x                                                             
  //      pitch = atan(-------------------------------)                                             
  //                    y * sin(roll) + z * cos(roll)                                               
  //                                                                                                
  // where:  x, y, z are returned value from accelerometer sensor                                   
  if (ay * sin(orientation[0]) + az * cos(orientation[0]) == 0)
    orientation[1] = ax > 0 ? (PI_F / 2) : (-PI_F / 2);
  else
    orientation[1] = (float)atan(-ax / (ay * sin(orientation[0]) + az * cos(orientation[0])));

  // heading: Rotation around the Z-axis. -180 <= roll <= 180                                       
  // a positive heading angle is defined to be a clockwise rotation about the positive Z-axis       
  //                                                                                                
  //                                       z * sin(roll) - y * cos(roll)                            
  //   heading = atan2(--------------------------------------------------------------------------)  
  //                    x * cos(pitch) + y * sin(pitch) * sin(roll) + z * sin(pitch) * cos(roll))   
  //                                                                                                
  // where:  x, y, z are returned value from magnetometer sensor                                    
  orientation[2] = (float)atan2(mz * sin(orientation[0]) - my * cos(orientation[0]), \
                                      mx * cos(orientation[1]) + \
                                      my * sin(orientation[1]) * sin(orientation[0]) + \
                                      mz * sin(orientation[1]) * cos(orientation[0]));


  // Convert angular data to degree 
  orientation[0] = orientation[0] * 180 / PI_F;
  orientation[1] = orientation[1] * 180 / PI_F;
  orientation[2] = orientation[2] * 180 / PI_F;

  return true;
}



int main()
{
    
    timer_led.start();
    pulse_timer.start();
    pc.baud(BAUD_RATE);
    hih6130.frequency(I2C_FREQUENCY);
    float orient[3] = {0};  
    init();
    
    
    timer.start();
    float roll_bias = 0;
    float pitch_bias = 0;
    float yaw_bias = 0;
    
    for (int i = 0; i < 500; i++){
        getOrientation(orient);
        roll_bias += orient[0];
        pitch_bias += orient[1];
        yaw_bias += orient[2];
    }      
    roll_bias = roll_bias / 500;
    pitch_bias = pitch_bias / 500;
    yaw_bias = yaw_bias / 500;
    
    while(1)
    {
        flex_sensor_read = f1.read();
        
        if (flex_sensor_read < 0.62){
          txBuffer[9] = 1;
          txBuffer[9] = (f3.read() < 0.66 ? 2 : txBuffer[9]);
        }
        else{
          txBuffer[9] = 0;
        }
        
        rxLen = mrf.Receive(rxBuffer, 128);
        if(rxLen){
          if (rxBuffer[8] == 20){
            led1 = led1^1;
          }        
        }
        // Get the orientation    
        getOrientation(orient);
        if(timer.read_ms() >= 100){
          timer.reset();
          txBuffer[8] = 19; //imu
          
          // Convert roll, pitch and yaw and convert it into x-y-z cooridinates
          int roll = (int)orient[0] - roll_bias;
          int pitch = (int)orient[1] - pitch_bias;
          int yaw = (int)orient[2] - yaw_bias;
          
          float x = 100 * cos(yaw * M_PI / 180)*cos(roll * M_PI / 180) + 100;
          float y = 100 * sin(yaw * M_PI / 180)*cos(roll * M_PI / 180) + 100;
          float z = 100 * sin(roll * M_PI / 180) + 100;
        
          txBuffer[10] = (uint8_t) y;
          txBuffer[11] = (uint8_t) z;
          txBuffer[12] = pulse();
          //pc.printf("Roll: %d, Pitch: %d, Yaw: %d\n\r", roll, pitch, heading);
          //pc.printf("roll: %d | pitch: %d | heading: %d | Trigger: %d\r\n ", txBuffer[10], txBuffer[11], heading, txBuffer[9]);
          pc.printf("x: %.2f, y: %.2d, z: %.2d\n\r",x, txBuffer[10], txBuffer[11]);  
          mrf.Send(txBuffer, 13);
        }
        // Update the colors array.
        uint32_t time = timer_led.read_ms();       
        for(int i = 0; i < LED_COUNT; i++)
        {
            uint8_t phase = (time >> 4) - (i << 2);
            colors[i] = hsvToRgb(phase / 256.0, 1.0, 1.0);
        }
    
        // Send the colors to the LED strip.
        ledStrip1.write(colors, LED_COUNT);
        ledStrip2.write(colors, LED_COUNT);
        ledStrip3.write(colors, LED_COUNT);
        ledStrip4.write(colors, LED_COUNT);
        
        //printf("f1: %.2f, f2: %.2f, f3: %.2f, f4: %.2f\n\r", f1.read(), f2.read(), f3.read(), f4.read());
        wait_ms(10);
    }
}
