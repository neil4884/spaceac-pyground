String ch433 = "";
String ch868 = "";
String ch915 = "";

void setup() {
    
    Serial.begin(9600); //COM
    Serial1.begin(9600); //GPS
    Serial3.begin(9600); //433
    Serial4.begin(9600); //868
    Serial5.begin(57600); //915

    Serial.println("Serial Started!");

}

void loop() {
    
    if(Serial3.available()) {
        char s1 = Serial3.read();
        ch433 += String(s1);
        int a1 = ch433.indexOf("$PSG$");
        if(a1 > 1) {
            Serial.print(ch433);
            ch433 = "";
        }
    } 
    
    if(Serial4.available()) {
        char s2 = Serial4.read();
        ch868 += String(s2);
        int a2 = ch868.indexOf("$PSG$");
        if(a2 > 1) {
            Serial.print(ch868);
            ch868 = "";
        }
    }
    
    if(Serial5.available()) {
        char s3 = Serial5.read();
        ch915 += String(s3);
        int a3 = ch915.indexOf("$PSG$");
        if(a3 > 1) {
            Serial.print(ch915);
            ch915 = "";
        }
    }
}
