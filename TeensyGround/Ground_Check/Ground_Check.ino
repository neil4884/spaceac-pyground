#include<TinyGPS++.h>
#include <MPU9255.h>

#define g 9.81
#define magnetometer_cal 0.06
#define acc_div 16384.0
#define gyr_div 131.0
#define alpha_a  0.8
#define alpha_g  0.5 
#define alpha_m  0.7
#define magnetometer_cal 0.06
#define yaw_axis_correc 90
#define toDeg 57.3
#define toRad 0.01745200698

#define magCalx 9.81
#define magCaly 24.725
#define magCalz -27.395

TinyGPSPlus gps;
MPU9255 mpu;

double ax,ax_F,ax_F_prev,ay,ay_F,ay_F_prev,az,az_F,az_F_prev;
double gx,gx_F,gx_prev,gx_prev_F,gy,gy_F,gy_prev,gy_prev_F,gz,gz_F,gz_prev,gz_prev_F;
double roll, pitch, yaw, yaw_F;
double mx,my,mz;
double mx_h, my_h;
double mx_max,my_max,mz_max = -100000;
double mx_min,my_min,mz_min = 100000;

String ch433 = "";
String ch868 = "";
String ch915 = "";
String ch001 = "";
String mylat = "";
String mylon = "";
String myalt = "";

double low_pass_filter(double val, double prev_filtered_val, double alpha) {
    double filtered_val;
    filtered_val = (1-alpha)*val+alpha*prev_filtered_val;
    return filtered_val;     
}
  
double high_pass_filter(double val,double prev_val, double prev_filtered_val, double alpha) {
    double filtered_val;
    filtered_val = (1-alpha)*prev_filtered_val+(1-alpha)*(val-prev_val);
    return filtered_val;
}

double process_magnetic_flux(int16_t input, double sensitivity) {
    return (input*magnetometer_cal*sensitivity)/0.6;
}

void calibrate_mag();

void setup() {

    pinMode(21, INPUT); // SWITCH
    pinMode(10, OUTPUT); //BUZZER
    pinMode(11, OUTPUT); //LED1
    pinMode(12, OUTPUT); //LED2

    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(500);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    delay(80);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(80);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    delay(80);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(80);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    delay(80);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(80);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    delay(80);
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(80);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    delay(800);

    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    delay(160);
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);

    Serial.begin(9600); //COM
    Serial1.begin(9600); //GPS
    Serial3.begin(9600); //433
    Serial4.begin(9600); //868
    Serial5.begin(57600); //915

    Serial.println("Serial Started!");

    mpu.init();

    mpu.set_acc_scale(scale_2g);
    mpu.set_gyro_scale(scale_250dps);
    
    mpu.read_acc();
    mpu.read_gyro();
    mpu.read_mag();

    ax = mpu.ax;
    ax_F_prev = low_pass_filter(ax, ax, alpha_a);
    ay = mpu.ay;
    ay_F_prev = low_pass_filter(ay, ay, alpha_a);
    az = mpu.az;
    az_F_prev = low_pass_filter(az, az, alpha_a);
    
    gx = mpu.gx;
    gx_prev = mpu.gx;
    gx_prev_F = high_pass_filter(gx,gx_prev, gx, alpha_g);
    gy = mpu.gy;
    gy_prev = mpu.gy;
    gy_prev_F = high_pass_filter(gy,gy_prev, gy, alpha_g);
    gz = mpu.gz;
    gz_prev = mpu.gz;
    gz_prev_F = high_pass_filter(gz,gz_prev, gz, alpha_g);
    
    mx = process_magnetic_flux(mpu.mx,mpu.mx_sensitivity) - magCalx;
    my = process_magnetic_flux(mpu.my,mpu.my_sensitivity) - magCaly;
    mz = process_magnetic_flux(mpu.mz,mpu.mz_sensitivity) - magCalz;
    
    yaw = atan2(my,mx)*toDeg;

    calibrate_mag();

}

void loop() {

    mpu.read_acc();
    mpu.read_gyro();
    mpu.read_mag();

    ax = mpu.ax;
    ay = mpu.ay;
    az = mpu.az;

    //roll = atan2(ay_F , az_F) * toDeg; // deg
    //pitch = atan2((- ax_F) , sqrt(ay_F * ay_F + az_F * az_F)) * toDeg; // deg
    
    pitch = atan2(ax_F,az_F)*toDeg;
    roll = atan2(ay_F,az_F)*toDeg;

    ax_F = low_pass_filter(ax, ax_F_prev, alpha_a);
    ay_F = low_pass_filter(ay, ay_F_prev, alpha_a);
    az_F = low_pass_filter(az, az_F_prev, alpha_a);
    
    mx = low_pass_filter(mx, process_magnetic_flux(mpu.mx,mpu.mx_sensitivity) - magCalx, alpha_m);
    my = low_pass_filter(mx, process_magnetic_flux(mpu.my,mpu.my_sensitivity) - magCaly, alpha_m);
    mz = low_pass_filter(mx, process_magnetic_flux(mpu.mz,mpu.mz_sensitivity) - magCalz, alpha_m);

    mx_h = my*cos(pitch*toRad) + mx*sin(pitch*toRad)*sin(roll*toRad) + mz*sin(pitch*toRad)*cos(roll*toRad);
    my_h = mx*cos(roll*toRad) + mz*sin(roll*toRad);

    yaw = atan2(-my_h, mx_h) * toDeg;

    ax_F_prev = ax_F;
    ay_F_prev = ay_F;
    az_F_prev = az_F;

    gx = mpu.gx;
    gy = mpu.gy;
    gz = mpu.gz;

    gx_F = high_pass_filter(gx,gx_prev, gx_prev_F, alpha_g);
    gy_F = high_pass_filter(gy,gy_prev, gy_prev_F, alpha_g);
    gz_F = high_pass_filter(gz,gz_prev, gz_prev_F, alpha_g);

    gx_prev = gx;
    gy_prev = gy;
    gz_prev = gz;

    gx_prev_F = gx_F;
    gy_prev_F = gy_F;
    gz_prev_F = gz_F;

    if(Serial1.available()) {
        while(Serial1.available()>0) {
            gps.encode(Serial1.read());
        }
        
        if(gps.location.isValid()) {
            mylat = String(gps.location.lat(), 6);
            mylon = String(gps.location.lng(), 6);
            myalt = String(gps.altitude.meters(), 2);
        }
        
        ch001 += "$PSG-I$F001$a";
        ch001 += mylat;
        ch001 += "$b";
        ch001 += mylon;
        ch001 += "$x";
        ch001 += String(180-roll);
        ch001 += "$y";
        ch001 += String(180-pitch);
        ch001 += "$z";
        ch001 += String(90+yaw);
        ch001 += "$r";
        ch001 += myalt;
        ch001 += "$PSG$";
        Serial.println(ch001);
        ch001 = "";
    }
    
    if(Serial3.available()) {
        char s1 = Serial3.read();
        ch433 += String(s1);
        int a1 = ch433.indexOf("$PSG$");
        if(a1 > 1) {
            ch433 += String('\n');
            Serial.print(ch433);
            ch433 = "";
            digitalWrite(10, HIGH);
            digitalWrite(11, HIGH);
            digitalWrite(12, HIGH);
            delay(50);
            digitalWrite(10, LOW);
            digitalWrite(11, LOW);
            digitalWrite(12, LOW);
        }
    } 
    
    if(Serial4.available()) {
        char s2 = Serial4.read();
        ch868 += String(s2);
        int a2 = ch868.indexOf("$PSG$");
        if(a2 > 1) {
            ch868 += String('\n');
            Serial.print(ch868);
            ch868 = "";
            digitalWrite(10, HIGH);
            digitalWrite(12, HIGH);
            delay(50);
            digitalWrite(10, LOW);
            digitalWrite(12, LOW);
        }
    }
    
    if(Serial5.available()) {
        char s3 = Serial5.read();
        ch915 += String(s3);
        int a3 = ch915.indexOf("$PSG$");
        if(a3 > 1) {
            ch915 += String('\n');
            Serial.print(ch915);
            ch915 = "";
            digitalWrite(10, HIGH);
            digitalWrite(11, HIGH);
            delay(50);
            digitalWrite(10, LOW);
            digitalWrite(11, LOW);
        }
    }
    
}

void calibrate_mag() {
    for (int i = 0;i<10000;i++) {
        if (mx > mx_max) {
            mx_max = mx;
        }
        
        if (my > my_max) {
            my_max = my;
        }
        
        if (mz > mz_max) {
            mz_max = mz;
        }


        if (mx < mx_min) {
            mx_min = mx;
        }
        
        if (my < my_min) {
            my_min = my;
        }
        
        if (mz < mz_min) {
        mz_min = mz;
        }
    }
}
