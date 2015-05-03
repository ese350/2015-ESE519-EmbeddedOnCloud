/*
 * ESE 519 - Project
 * A Real Time Home Infotainment System
 * Team Members: Aditya Deshpande, Nishank Shinde, Cheng Cheng
 *
*/ 

#include "mbed.h"
#include "MRF24J40.h"

#define HIH6130_ADDRESS7BIT 0x27
#define HIH6130_ADDRESS8BIT 0x27 << 1
#define BAUD_RATE 9600
#define I2C_FREQUENCY 400000

Serial pc (USBTX, USBRX);

I2C hih6130(p9,p10);
          
MRF24J40 mrf(p11, p12, p13, p14, p21);  //RF transceiver
    
DigitalOut led1(LED1);                  //LED1
DigitalOut led2(LED2);                  //LED2
DigitalOut led3(LED3);                  //LED3
DigitalOut led4(LED4);                  //LED4

DigitalOut p_30(p30);
DigitalOut p_29(p29);
  
PwmOut p_26(p26);
PwmOut p_25(p25);
PwmOut p_22(p22);
PwmOut p_23(p23);
  
Timer timer;                            // To send data to the central node after regular intervals
  
AnalogIn ain(p20);  
  
// Send / receive buffers.
// IMPORTANT: The MRF24J40 is intended as zigbee tranceiver; it tends
// to reject data that doesn't have the right header. So the first 
// 8 bytes in txBuffer look like a valid header. The remaining 120
// bytes can be used for anything you like.
uint8_t txBuffer[128]= {1, 8, 0, 0xA1, 0xB2, 0xC3, 0xD4, 0x00};
uint8_t rxBuffer[128];
uint8_t rxLen;

uint8_t pulse = 0;

// Get the temperature and humidity
void temperature_humidity(uint8_t *temperature, uint8_t *humidity){
      
      uint16_t humidity_count    = 0;
      uint16_t temperature_count = 0;
      uint8_t  val[4]            = {0};
      
      hih6130.start();
      unsigned int ack = hih6130.write(HIH6130_ADDRESS8BIT);
      if (ack != 1){
        pc.printf("No MR ack %d\n\r", ack);
      }
      else{
          hih6130.stop();
      }
      
      unsigned int data_ack = hih6130.read(HIH6130_ADDRESS8BIT, (char *)val, 4);
      if (data_ack != 0){
          pc.printf("No data ack %d\n\r",data_ack);
      }
      
      humidity_count    = ((val[0] & 0x3F) << 8 | val[1]);
      temperature_count = ((val[2]) << 6 | ((val[3] & 0xF6) >> 2));
      
      *humidity    = (uint8_t)((humidity_count * 100) / 16383);
      *temperature = (uint8_t)(((temperature_count * 165) / 16383) - 40);
}

// Not actual noise - only for debugging
uint8_t noise(void){
    uint8_t noise = rand() % 10;
    return noise;
}

// Get the light intensity
uint8_t light(void){
    uint8_t light = (uint8_t)(ain.read() * 10);
    return light;
}        

// Set the Light intensity and the fan speed
void setLightandFan(uint8_t val){
    uint8_t fan_val   = val / 10;
    uint8_t light_val = val % 10;
    
    float light_duty  = (float)light_val / 10.0;
    float fan_duty    = (float)fan_val / 10.0;
    
    pc.printf("Fan: %d, Light: %d \r\n",fan_val, light_val);
    
    p_26.write(light_duty);
    p_25.write(light_duty);
    p_22.write(fan_duty);
    p_23.write(light_duty);
    
}
          
int main (void)
{
  p_30 = 1;
  p_29 = 0;
  
  uint8_t destination_address = 18;   
  pc.baud(BAUD_RATE);
  hih6130.frequency(I2C_FREQUENCY);
  timer.start();
  while(1)
  {
    // Check if any data was received. 
    rxLen = mrf.Receive(rxBuffer, 128);
    if(rxLen) 
    {
      if (rxBuffer[8] == 17){
        led1 = led1^1;
        setLightandFan(rxBuffer[9]);
      }  
      if (rxBuffer[8] == 19){
          led1 = led1^1;
          pulse = rxBuffer[12];
      }    
    }
    else{
      if (timer.read_ms() > 400){
        destination_address = 18;
      }
    }       
          
    /* Each second, send environmental data. */
    if(timer.read_ms() >= 500){
      timer.reset();
      led2 = led2^1;
      txBuffer[8] = destination_address;
      /* Set Temperature, Humidity, Noise, Light */
      txBuffer[10] = noise();
      txBuffer[11] = light();
      temperature_humidity(&txBuffer[9], &txBuffer[12]);
      txBuffer[13] = pulse;
      
      //pc.printf("%d %d %d %d\n\r",txBuffer[8], txBuffer[9], txBuffer[10], txBuffer[11]);
      mrf.Send(txBuffer, 14);
    }
  }
  
}
 