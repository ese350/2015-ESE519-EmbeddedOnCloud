/*
 * ESE 519 - Final Project
 * A Realtime Home infotainment system
 * Team Members: Aditya Deshpande, Cheng Cheng, Nishank Shinde
 * communication_central.cpp 
*/ 

#include "mbed.h"
#include "MRF24J40.h"
  
MRF24J40 mrf(p11, p12, p13, p14, p21);
  
// LEDs
DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);
  
  
// Serial port for showing RX data.
Serial pc(USBTX, USBRX); 
  
// Send / receive buffers.
// IMPORTANT: The MRF24J40 is intended as zigbee tranceiver; it tends
// to reject data that doesn't have the right header. So the first 
// 8 bytes in txBuffer look like a valid header. The remaining 120
// bytes can be used for anything you like.
uint8_t txBuffer[128]= {1, 8, 0, 0xA1, 0xB2, 0xC3, 0xD4, 0x00};
  
uint8_t rxBuffer[128];
uint8_t rxLen;
  
  
int main (void){
  pc.baud(9600);
  while(1){
    rxLen = mrf.Receive(rxBuffer, 128);
    if(rxLen){
      led1 = !led1;
      // Data from glove
      if (rxBuffer[8] == 19){
        pc.printf("0x%02X,0x%02X,0x%02X,0x%02X", rxBuffer[8],rxBuffer[9],rxBuffer[10],rxBuffer[11]);
        
      }
      
      // Data from the sensor node
      if (rxBuffer[8] == 18){
        pc.printf("0x%02X,0x%02X,0x%02X,0x%02X,0x%02X,0x%02X", rxBuffer[8], rxBuffer[9],rxBuffer[10],rxBuffer[11],rxBuffer[12],rxBuffer[13]);
        wait(0.2);
      }      
    }
    
    // To send the fan and light control parameters back to the sensor node
    if (pc.readable()){
      uint8_t x = pc.getc();
      txBuffer[8] = 17;
      txBuffer[9] = x;
      mrf.Send(txBuffer,10);
      led2 = !led2;
    }    
  }
}
 