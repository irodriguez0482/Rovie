//functions: 2 for data, 4 for 17, 1 for 23, 2 for buttons (remove with Pi connected)
void getSerialData();
void processData(String command);
void move17(int dir17); //calls rover movement
void forward();
void backward();
void left();
void right();
void plow(int dir23); //edit later when gears start working
//buttons
void force(); //force sensor
void eStop(); //E-stop button

//counts
int rot23=0; //keeps track of how much to rotate plow, iterates until rCount
int rCount=2; //change count to move plow more //2 is best
int level=0;
int max=20; //max level of plow
int min=-20; //minimum level of plow
//at half-speed, 5 moves it 2 inches.
//1 moves it 3/8 of an inch
//using 2 for 3/4 on an inch
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
int Pillpin=28; //Controls mosfet on/off for vibration

//force sensor
int bPin = 22;
int oPin = 24;
int gPin = A12;
int sPin = A13;

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
//force sensor
  pinMode(oPin, OUTPUT);
  pinMode(bPin, INPUT_PULLUP);  // Use internal pull-up resistor
//e-stop
  pinMode(sPin, OUTPUT);
  pinMode(gPin, INPUT_PULLUP);  // Use internal pull-up resistor

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
  eStop(); //check before processing, remove with Pi connected
  processData(data);
  force(); //check after processing, remove with Pi connected

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

    if(rCount==rot23){
      digitalWrite(enPin23,HIGH);
      data[3]=en23+47; //disables plow movement by rewriting received data
      Serial.println("ArduinoReady");
      }

    if((rot23<rCount) && (en23!=0)){
      digitalWrite(enPin23,LOW); //allows plow motors to operating
      plow(pDir);
      rot23=rot23+1;
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
      
      break;
    case 10:
      //specify 90 or 180
      left();
      
      break;
    case 11:
      //specify 90 or 180
      right();
      
      break;
    default:
      break;
  }

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
  
} 
void right(){ //currently a wide turn
  digitalWrite(dirPinR,HIGH);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(dirPinLweird,LOW);  

  //coded for half steps right now because gears are struggling, change if fixed 
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);
  /*
  //digitalWrite(enPinR,HIGH);
  digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction  
  digitalWrite(dirPinLweird,LOW);  

  //coded for half steps right now because gears are struggling, change later  
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  //need to double-check that this is the correct speed, it might be high high low 
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, HIGH); 
  digitalWrite(ms3PinR, LOW);
*/
}


void left(){ //currently a wide turn
 digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,LOW); // Enables the motor to move in a particular direction
  digitalWrite(dirPinLweird,HIGH);  

  //coded for half steps right now because gears are struggling, change if fixed 
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, LOW); 
  digitalWrite(ms3PinL, LOW);
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);
 /* 
 digitalWrite(dirPinR,LOW);  // Enables the motor to move in a particular direction                            
  digitalWrite(dirPinL,HIGH); // Enables the motor to move in a particular direction  
  digitalWrite(dirPinLweird,LOW);    
//need to double-check that this is the correct speed, it might be high high low  
  digitalWrite(ms1PinL, HIGH); 
  digitalWrite(ms2PinL, HIGH); 
  digitalWrite(ms3PinL, LOW);
  //coded for half steps right now because gears are struggling, change later
  digitalWrite(ms1PinR, HIGH); 
  digitalWrite(ms2PinR, LOW); 
  digitalWrite(ms3PinR, LOW);
 */
} 

void plow(int dir23){
  //nema23 
  if(dir23==0){        
    digitalWrite(dirPin23,LOW); // down
    if(rot23==0){
      level=level-1;  
    }
    if(level<min){
      digitalWrite(enPin23,HIGH);//allows for a max height
      Serial.println("Level cannot be changed"); 
    }
  }
  else{
    digitalWrite(dirPin23,HIGH); // up
    if(rot23==0){
      level=level+1;  
    }
    if(level>max){
      digitalWrite(enPin23,HIGH);//allows for a max height
      Serial.println("Level cannot be changed");
    } 
  }     
  //half-step for better precision                        
  digitalWrite(ms1Pin23, HIGH); 
  digitalWrite(ms2Pin23, LOW); 
  digitalWrite(ms3Pin23, LOW);

  //Serial.println("Plow");
  for(int x = 0; x < numSteps * 2 * rotations; x++) {  //times 2 cause half-step
    digitalWrite(stepPin23,HIGH);  
    delayMicroseconds(delay1);  
    digitalWrite(stepPin23,LOW);    
    delayMicroseconds(delay1);  
  } 

} 
//String oldData="000000";
//only use when not using Pi
void force(){ //force sensor
int buttonState = digitalRead(bPin);  // Read once, reuse
  if (buttonState == LOW) {
    Serial.println("Load detected");
    //oldData=data;
    //data="000110";
    processData("000110");
  }
}

void eStop(){ //E-stop button
  int stopState = digitalRead(gPin);  // Read once, reuse
  if (stopState == LOW) {
    Serial.println("E-stop pushed");
    data="000000";
  }
}
