/*
this goes on your arduino
for use with Processing example SimpleSerialArduinoscope

*/

#include <Wire.h>



void setup() {
  TCCR0B = TCCR0B & 0b11111000 | 0x01;
  TCCR1B = TCCR1B & 0b11111000 | 0x01;
  TCCR2B = TCCR2B & 0b11111000 | 0x01;
  pinMode(5, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(7, LOW);
  
  Serial.begin(115200);  
  
  Wire.begin();
  

  delay(1000);
  Serial.print("hallo ");
}

void loop() {  
  /*
  // read all analog ports, split by " "
  for (int i=0;i<6;i++){
    Serial.print(analogRead(i));
    Serial.print(" ");
  }*/
  
  // read analog ports using I2C
  const int I2C_address = 0x48;  // I2C write address 
  const byte DAT[8] = {0x8C,0xCC,0x9C,0xDC,0xAC,0xEC,0xBC,0xFC};
                                 // Constant configuration data


  byte Adval_High, Adval_Low;    // Store A/D value (high byte, low byte)
  int Adval = 0;
  byte i;                        // Counter

  for (i=0; i<=7; i++)

  {
    Wire.beginTransmission(I2C_address);
    Wire.send(DAT[i]);        // Configure the device to read each CH  
    Wire.endTransmission(); 
    delay(1);

    

    // Read A/D value

    Wire.requestFrom(I2C_address, 2);

    while(Wire.available())          // Checkf for data from slave
    { 
      Adval_High = Wire.receive();   // Receive A/D high byte
      Adval_Low = Wire.receive();    // Receive A/D low byte
    } 
    
    Adval = Adval_High << 8;

    if (Adval_Low > 0x0F)
    {
      Adval += Adval_Low;
    }

    Serial.print(Adval);
    Serial.print(" ");

  }  
  
  // read all digital ports, split by " "
  for (int i=2;i<14;i++){
    if (i==5){
      Serial.print(0);
    }
    else
    {
      Serial.print(0);
    }
    Serial.print(" ");
  }
  
  // frame is marked by LF
  Serial.println();
}
