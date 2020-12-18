unsigned long Time;

int cnt=1;
int hh=00;
int mm=00;
int ss=00;
double lat1=13.0000000;
double lon1=100.0000000;
float ap=850.00;
float ag=860.00;
float it=30.50;
float et=12.50;
float hu=84.50;
float ax=-1.000000;
float ay=-1.000000;
float az=-3.000000;
float tx=0.000000;
float ty=90.000000;
float tz=45.000000;
float mpxv=0.65;
float pm010=15.00;
float pm025=12.00;
float pm100=11.00;

void setup() {
    Serial3.begin(9600);
    Serial.begin(9600);
    
}

void loop() {
  Serial.println(MODE(4331));
  Serial.println(MODE(4332));
  delay(100);
  Serial.println(MODE(868));
  delay(50);
  Serial.println(MODE(915));
  delay(100);
  Serial.println(def());
  delay(2000);

}

String def() {
  String s;
  s = "$PSG-I$F001$a12.500000$b99.500000$x";
  if(tx>=360) {
    tx=0-360;
  }
  else {
    tx+=0.5;
  }
  
  if(ty>=360) {
    ty=0-360;
  }
  else {
    ty+=0.5;
  }
  
  if(tz>=360) {
    tz=0-360;
  }
  else {
    tz+=0.5;
  }
  s += String(tx, 2);
  s += "$y";
  s += String(ty, 2);
  s += "$z";
  s += String(tz, 2);
  s += "$r10.15$PSG$";
  return s;
}

String MODE(int freq) {
  String s;
  if(freq==4331) {
    s="$PSG-I";
    s+="$F433";
    s+=PKG_CNT();
    s+=SYS_TIM();
    s+=GPS_LAT();
    s+=GPS_LON();
    s+=ALT_BAR();
    s+=ALT_GPS();
    s+=INT_TMP();
  }
  else if(freq==4332) {
    s="";
    s+=INT_HUM();
    s+=GYR_0AX();
    s+=GYR_0AY();
    s+=GYR_0AZ();
    s+=GYR_0TX();
    s+=GYR_0TY();
    s+=GYR_0TZ();
    s+=MPXV();
    //s+="$PSG$";
  }
  else if(freq==868) {
    s="$PSG-I";
    s+="$F868";
    s+=PKG_CNT();
    s+=SYS_TIM();
    s+=GPS_LAT();
    s+=GPS_LON();
    s+=EXT_TMP();
    s+=PM1();
    s+=PM25();
    s+=PM10();
    s+="$PSG$";
  }
  else if(freq==915) {
    s="$PSG-I";
    s+="$F915";
    s+=PKG_CNT();
    s+=SYS_TIM();
    s+=ALT_BAR();
    s+=ALT_GPS();
    s+=GPS_LAT();
    s+=GPS_LON();
    s+="$PSG$";
  }
  return s;
}

String PKG_CNT() {
  return "$C"+String(cnt++);
}
String INT_TMP() {
  return "$S"+String(it+=0.01,2);
}
String EXT_TMP() {
  return "$K"+String(et+=0.01,2);
}
String SYS_TIM() {
  char BFFR[10];
  ss+=2;
  if(ss==60) {
    mm++;
    ss=0;
  }
  if(mm==60) {
    hh++;
    mm=0;
  }
  sprintf(BFFR,"%02d%02d%02d",hh,mm,ss);
  String s = "$T"+String(BFFR);
  return s;
}
String INT_HUM() {
  return "$H"+String(hu+=0.01,2);
}
String GPS_LAT() {
  return "$A"+String(lat1+=0.001,7);
}
String GPS_LON() {
  return "$B"+String(lon1-=0.001,7);
}
String GYR_0AX() {
  return "$X"+String(ax);
}
String GYR_0AY() {
  return "$N"+String(ay);
}
String GYR_0AZ() {
  return "$Z"+String(az);
}
String GYR_0TX() {
  return "$R"+String(tx);
}
String GYR_0TY() {
  return "$U"+String(ty);
}
String GYR_0TZ() {
  return "$Y"+String(tz);
}
String MPXV() {
  return "$V"+String(mpxv+=0.01,2);
}
String PM1() {
  return "$L"+String(pm010);
}
String PM25() {
  return "$M"+String(pm025);
}
String PM10() {
  return "$Q"+String(pm100);
}
String ALT_BAR() {
  return "$D"+String(ap+=0.5,2);
}
String ALT_GPS() {
  return "$E"+String(ap+=1.0,2);
}
