String str;
String ID;
String rssi;
void setup() {
  Serial.begin(230400); // opens serial port, sets data rate to 9600 bps
  Serial.setTimeout(1);
  Serial1.begin(230400);
  Serial1.setTimeout(3);
}
int x = 1;

String serial1Readln(){
  while(!Serial1.available()){
    __asm__ __volatile__ ("nop\n\t");
  }
  return Serial1.readString();
}

void loop() {
  Serial1.println("AT+DISI?");   //envio el comando
  str = serial1Readln();         // leo mensaje de comienzo de escaneo DISIS pero lo descarto
  str = serial1Readln();
  while (!str.endsWith("E")) {
    str = str.substring(17);    //  ignoro ciertos bytes que no son relevantes
    if (str.startsWith("BEACBEACBEACBEACBEACBEAC")) {   // filtro solo "nuestros" beacons (24)
      ID = str.substring(24,32);
      rssi = str.substring(58);
      Serial.println(ID);
      Serial.println(rssi);
    }
    str = serial1Readln();
  }
}
