//functions: 2 for data, 4 for 17, 1 for 23, 1 for pills
void getSerialData();
void processData(String command);
void move17(int dir17); //calls rover movement
void forward();
void backward();
void left();
void right();
void plow(int dir23); //edit later when gears start working
void pill(int pow); //will be written when pill circuit is actually determined, waiting on tests

//nema17's
//ms control step
int ms1Pin   = 5; 
int ms2Pin   = 6;
int ms3Pin   = 7;
//for (ms1,ms2,ms3), steps are:
// Full=(low,low,low)
// 1/2=(high,low,low)
// 1/4=(low,high,low)
// 1/8=(high,high,low)
// 1/16=(low,low,high)
// 1/32=(low,high,high) or (high,high,high)
int enPin = A0; //pin for enabling or disabling motors
// defines pins 
#define stepPin 4    //frequency of stepping
#define dirPinR  2   //direction of right motors
#define dirPinL  3   //direction of left motors
//set dir high for clockwise, low for ccw

//nema23's
int ms1Pin23 =10;
int ms2Pin23 =11;
int ms3Pin23 = 12;
int enPin23 = A2;
int rot23=0; //keeps track of how much to rotate plow
#define stepPin23 9
#define dirPin23 8

//pills
int Pillpin=14; //change later

int numSteps = 200;  // 360/1.8 degree = 200 - NEMA17 no reduction 
int rotations = 1;   // Number of rotations of the rotor for each 
int delay1  =   700; // Microdelay between coil activations (us) 
int delay2  =   1000;// Normal delay (ms) 

void setup() { 
  Serial.begin(9600); 
  //nema17s pinmodes
  pinMode(ms1Pin,OUTPUT);  // MS1 set to receive Arduino signals 
  pinMode(ms2Pin,OUTPUT);  // MS2 set to receive Arduino signals 
  pinMode(ms3Pin,OUTPUT);  // MS3 set to receive Arduino signals 

  pinMode(stepPin,OUTPUT);  
  pinMode(dirPinL,OUTPUT); 
  pinMode(dirPinR,OUTPUT); 

  pinMode(enPin,OUTPUT);
//nema23 pinmodes
  pinMode(ms1Pin23,OUTPUT);
  pinMode(ms2Pin23,OUTPUT);
  pinMode(ms3Pin23,OUTPUT);
  pinMode(stepPin23,OUTPUT);
  pinMode(dirPin23,OUTPUT);
  pinMode(enPin23,OUTPUT);
//pill
  pinMode(Pillpin,OUTPUT);
  Serial.println("2ArduinoReady3");
} 



int en17=0; //Will take input from Pi, turns wheel motors on and off
int en23=0; //will take input from Pi, turn plow motor on and off
int enPill=0; //will take input from Pi, turn pills on and off
int m17=0; //for nema17 movement
int pDir=0;

void loop() { 
  getSerialData();
  //ideally, should get 1 byte, with each digit meaning something
    //first bit sets nema17 en (0 off, 1 on)
    //second and third bits, direction of rover
      // forward (00), backward (01), left(10), right(11)
    //fourth bit, sets nema23 en (0 off, 1 on)
    //fifth bit, lifts nema23 up (0) or down (1)
    //sixth bit, turns vibration motors off (0) or on (1)
    //two extra bits, could use for speed of forward or backward. Eva, lmk what you think
  //processData();
  
} 
String data="000000";
void getSerialData(){
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
  processData(data);

}

void processData(String command){
  //if(data!="000000"){
    en17=command[0]-48; //enables wheel motors
    m17=(command[1]-48)*10+(command[2]-48); //forward, backward, left, or right
    en23=command[3]-48; //enables plow movement
    pDir=command[4]-48; //sets plow up or down
    enPill=command[5]-48;//sets pills on or off
  //}
    //motors on or off
    //will also have if statement for pills, which will determine if they get called or not       
      pill(enPill);
    if(en17==0){
      digitalWrite(enPin,HIGH); //turns wheel motors off
    }
    else{
      digitalWrite(enPin,LOW); //allows wheel motors to operating
      move17(m17); //could edit later to take speed, but should only want 1 speed anyway.
    }       
    if(en23==0){
      digitalWrite(enPin23,HIGH); //turns plow motors off
      rot23=0; //resets plow so that it can rotate again
    }
    else{
      digitalWrite(enPin23,LOW); //allows plow motors to operating
      plow(pDir); 
    } 

    //for now, will just code forward and up, but direction will be set by serial communication     
}

void move17(int dir17){
  switch (dir17) {
    case 00:
      forward();
      Serial.println("forward");
      break;
    case 01:
      backward();
      Serial.println("backward");
      break;
    case 10:
      left();
      Serial.println("left");
      break;
    case 11:
      right();
      Serial.println("right");
      break;
    default:
      break;
  }

}
void forward(){
  
  digitalWrite(dirPinR,HIGH);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,LOW); // Enables the motor to move in a particular direction  

  //coded for half steps right now because gears are struggling, change later  
  digitalWrite(ms1Pin, HIGH); 
  digitalWrite(ms2Pin, LOW); 
  digitalWrite(ms3Pin, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin,HIGH);   
    delayMicroseconds(delay1); 
    digitalWrite(stepPin,LOW);     
    delayMicroseconds(delay1);  
  }  
}

void backward(){
  
  digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction   
  digitalWrite(ms1Pin, HIGH); 
  digitalWrite(ms2Pin, LOW); 
  digitalWrite(ms3Pin, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin,HIGH);   
    delayMicroseconds(delay1); 
    digitalWrite(stepPin,LOW);     
    delayMicroseconds(delay1);  
  } 
} 
void right(){
  
  digitalWrite(dirPinR,HIGH);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction  

  //coded for half steps right now because gears are struggling, change later  
  digitalWrite(ms1Pin, HIGH); 
  digitalWrite(ms2Pin, LOW); 
  digitalWrite(ms3Pin, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin,HIGH);   
    delayMicroseconds(delay1); 
    digitalWrite(stepPin,LOW);     
    delayMicroseconds(delay1);  
  }  
}

void left(){
  
  digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,LOW); // Enables the motor to move in a particular direction   
  digitalWrite(ms1Pin, HIGH); 
  digitalWrite(ms2Pin, LOW); 
  digitalWrite(ms3Pin, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin,HIGH);   
    delayMicroseconds(delay1); 
    digitalWrite(stepPin,LOW);     
    delayMicroseconds(delay1);  
  } 
} 

void plow(int dir23){
  //nema23     
  if(dir23==0){        
  digitalWrite(dirPin23,LOW); // up  
  }
  else{
    digitalWrite(dirPin23,HIGH); // down
  }                             
  digitalWrite(ms1Pin23, LOW); 
  digitalWrite(ms2Pin23, LOW); 
  digitalWrite(ms3Pin23, LOW);

  while(rot23<15){ //keeps plow from moving too far up or down, experiments will determine how much to move
  Serial.println("Plow"); 
  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 1 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin23,HIGH);  
    delayMicroseconds(delay1);  
    digitalWrite(stepPin23,LOW);    
    delayMicroseconds(delay1);  
  } 
  rot23=rot23+1;
  }
} 

void pill(int pow){
  if(pow==1){
    digitalWrite(Pillpin, HIGH);
  }
  else{
    digitalWrite(Pillpin, LOW);
  }
}
  else{
    digitalWrite(Pillpin, LOW);
  }
}
