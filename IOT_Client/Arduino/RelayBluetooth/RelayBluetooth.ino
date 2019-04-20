#include <SoftwareSerial.h>
const int relay_pin = 8;

SoftwareSerial mySerial(15, 14); // RX, TX


void setup()
{
  Serial.begin(9600);
  pinMode(relay_pin, OUTPUT);
  Serial.println("Goodnight moon!");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  digitalWrite(relay_pin, HIGH);
}

// The loop function is called in an endless loop
void loop()
{

  char serial_ch=0;
  if (mySerial.available())
  {
    String str_bt = mySerial.readString();
    Serial.println(str_bt);
    str_bt.trim();
    if(str_bt=="True")
    {
      Serial.println("Trun On Computer");
      digitalWrite(relay_pin,LOW);
      delay(500);
      digitalWrite(relay_pin,HIGH);
      mySerial.println(" COM_OK");

    }
    else if(str_bt=="False")
    {
      Serial.println("Trun Off Computer(Shoud be deleted )");
      //digitalWrite(relay_pin,LOW);
    }

  }

  if (Serial.available())
  {
    serial_ch= Serial.read();
    if (serial_ch == 'a')
    {
      digitalWrite(relay_pin,LOW);
      delay(500);
      digitalWrite(relay_pin,HIGH);
    }

    Serial.print(serial_ch);
    mySerial.write(serial_ch);
  }





}
