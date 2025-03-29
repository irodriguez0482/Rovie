//functions: 2 for data, 4 for 17, 1 for 23
void getSerialData();
void processData(String command);
void move17(int dir17); //calls rover movement
void forward();
void backward();
void left();
void right();
void plow(int dir23); //edit later when gears start working

//counts
int rot23=0; //keeps track of how much to rotate plow, iterates until rCount
int rCount=15; //change count to move plow more
//will also have turn counts, WIP

//serial communication bits
int en17=0; //Will take input from Pi, turns wheel motors on and off
int en23=0; //will take input from Pi, turn plow motor on and off
int enPill=0; //will take input from Pi, turn pills on and off
int m17=0; //for nema17 movement
int pDir=0;

//nema17's
//left
#define dirPinL  2   //direction of right motors
#define stepPinL 3    //frequency of stepping
int ms1PinL   = 4; 
int ms2PinL   = 5;
int ms3PinL   = 6;
int enPinL = A4; //pin for enabling or disabling motors
#define dirPinLweird A6 //one of the motors goes weird ways, code individually

//right
#define dirPinR  8   //direction of left motors
#define stepPinR 9    //frequency of stepping
int ms1PinR   = 10; 
int ms2PinR   = 11;
int ms3PinR   = 12;
int enPinR = A0; //pin for enabling or disabling motors

//nema23
#define dirPin23 42
#define stepPin23 44
int ms1Pin23 =46;
int ms2Pin23 =48;
int ms3Pin23 = 50;
int enPin23 = A2;


//pills
int Pillpin=A5; //change later, and add one more

//motor info
int numSteps = 200;  // 360/1.8 degree = 200 - NEMA17 no reduction 
int rotations = 1;   // Number of rotations of the rotor for each 
int delay1  =   700; // Microdelay between coil activations (us) 
int delay2  =   1000;// Normal delay (ms) 

void setup() { 
  Serial.begin(9600); 
  //nema17s pinmodes
  pinMode(ms1PinL,OUTPUT);  // MS1 set to receive Arduino signals 
  pinMode(ms2PinL,OUTPUT);  // MS2 set to receive Arduino signals 
  pinMode(ms3PinL,OUTPUT);  // MS3 set to receive Arduino signals 
  pinMode(stepPinL,OUTPUT);  
  pinMode(dirPinL,OUTPUT); 
  pinMode(enPinL,OUTPUT);
  pinMode(dirPinLweird, OUTPUT);

  pinMode(ms1PinR,OUTPUT);  // MS1 set to receive Arduino signals 
  pinMode(ms2PinR,OUTPUT);  // MS2 set to receive Arduino signals 
  pinMode(ms3PinR,OUTPUT);  // MS3 set to receive Arduino signals 
  pinMode(stepPinR,OUTPUT);  
  pinMode(dirPinR,OUTPUT); 
  pinMode(enPinR,OUTPUT);

//nema23 pinmodes
  pinMode(ms1Pin23,OUTPUT);
  pinMode(ms2Pin23,OUTPUT);
  pinMode(ms3Pin23,OUTPUT);
  pinMode(stepPin23,OUTPUT);
  pinMode(dirPin23,OUTPUT);
  pinMode(enPin23,OUTPUT);
//pill
  pinMode(Pillpin,OUTPUT);
  //will have another pin when the 16th gets added
  Serial.println("ArduinoReady");
} 


void loop() { 
  getSerialData();
  //ideally, should get 1 byte, with each digit meaning something
    //first bit sets nema17 en (0 off, 1 on)
    //second and third bits, direction of rover
      // forward (00), backward (01), left(10), right(11)
    //fourth bit, sets nema23 en (0 off, 1 on)
    //fifth bit, lifts nema23 up (0) or down (1)
    //sixth bit, turns vibration motors off (0) or on (1)
    //seventh bit, tell if turns are 90* or 180*, different types of turns  
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

    //turn pill off before moving plow      
    if(enPill==0){
      digitalWrite(Pillpin, LOW);
    } 

    if(en23==0){
      digitalWrite(enPin23,HIGH); //turns plow motors off
      rot23=0; //resets plow so that it can rotate again
    }
    else{
      digitalWrite(enPin23,LOW); //allows plow motors to operating
      plow(pDir); 
    }

    //dont turn on pill until plow has moved
    if(enPill==1){
      digitalWrite(Pillpin, HIGH);
    } 

    //nema
    if(en17==0){
      digitalWrite(enPinL,HIGH); //turns wheel motors off
      digitalWrite(enPinR,HIGH); //turns wheel motors off
    }
    else{
      digitalWrite(enPinL,LOW); //allows wheel motors to operate
      digitalWrite(enPinR,LOW); //allows wheel motors to operate
      move17(m17); //could edit later to take speed, but should only want 1 speed anyway.
    } 
    
}

void move17(int dir17){
  switch (dir17) {
    case 00:
      forward();
      //Serial.println("forward");
      break;
    case 01:
      backward();
      //Serial.println("backward");
      break;
    case 10:
      //specify 90 or 180
      left();
      //Serial.println("left");
      break;
    case 11:
      //specify 90 or 180
      right();
      //Serial.println("right");
      break;
    default:
      break;
  }

}

//for (ms1,ms2,ms3), steps are:
// Full=(low,low,low)
// 1/2=(high,low,low)
// 1/4=(low,high,low)
// 1/8=(high,high,low)
// 1/16=(low,low,high)
// 1/32=(low,high,high) or (high,high,high)

void forward(){
  
  digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(dirPinLweird,LOW);  

  //coded for half steps right now because gears are struggling, change if fixed 
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPinL,HIGH);   
    digitalWrite(stepPinR,HIGH);
    delayMicroseconds(delay1); 
    digitalWrite(stepPinL,LOW);
    digitalWrite(stepPinR,LOW);     
    delayMicroseconds(delay1);  
  }  
}

void backward(){
  
  digitalWrite(dirPinR,HIGH);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,LOW); // Enables the motor to move in a particular direction 
  digitalWrite(dirPinLweird,HIGH);    
  //coded for half steps right now because gears are struggling, change if fixed  
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPinL,HIGH);   
    digitalWrite(stepPinR,HIGH);
    delayMicroseconds(delay1); 
    digitalWrite(stepPinL,LOW);
    digitalWrite(stepPinR,LOW);     
    delayMicroseconds(delay1);  
  }  
} 
void right(){ //currently a wide turn
  //digitalWrite(enPinR,HIGH);
  digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction  
  digitalWrite(dirPinLweird,LOW);  

  //coded for half steps right now because gears are struggling, change later  
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  //need to double-check that this is the correct speed, it might be high high low 
  digitalWrite(ms1PinR, LOW); 
  digitalWrite(ms2PinR, HIGH); 
  digitalWrite(ms3PinR, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPinL,HIGH);   
   digitalWrite(stepPinR,HIGH);

    delayMicroseconds(delay1); 

    digitalWrite(stepPinL,LOW);
    digitalWrite(stepPinR,LOW);

    delayMicroseconds(delay1);  
  } 
 
}


void left(){ //currently a wide turn
  
 digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction  
  digitalWrite(dirPinLweird,LOW);    
//need to double-check that this is the correct speed, it might be high high low  
  digitalWrite(ms1PinL, LOW); 
  digitalWrite(ms2PinL, HIGH); 
  digitalWrite(ms3PinL, LOW);
  //coded for half steps right now because gears are struggling, change later
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);

  // For loop makes 200 * 1 pulses for making one full cycle rotation 
  
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPinL,HIGH);   
    digitalWrite(stepPinR,HIGH);

    delayMicroseconds(delay1); 

    digitalWrite(stepPinL,LOW);
    digitalWrite(stepPinR,LOW);

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

  while(rot23<rCount){ //keeps plow from moving too far up or down, experiments will determine how much to move 
  //Serial.println("Plow");
  for(int x = 0; x < numSteps * 1 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin23,HIGH);  
    delayMicroseconds(delay1);  
    digitalWrite(stepPin23,LOW);    
    delayMicroseconds(delay1);  
  } 
  rot23=rot23+1;
  if(rot23==rCount){
    Serial.println("ArduinoReady");
  }
  }
} 