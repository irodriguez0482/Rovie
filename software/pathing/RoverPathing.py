# basic rover path for 3x3 meter area
#   -moves forward 3 meters
#   -180 turn right with radius ~0.5m
#   -move forward 3 meters
#   -180 turn left with radius ~0.5m
#   -repeat until 6 passes

import testmodule
import serial
import time
import MotorCom
import ForceButton

SERIAL_PORT = "/dev/ttyACM0"  # Update if necessary (e.g., "COM3" for Windows)
BAUD_RATE = 9600
ROVER_LENGTH = 1    #TEMP VALUES in Meters
ROVER_WIDTH = 1

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)   
except serial.SerialException as e:
    print("[ERROR] Serial communication issue:", e)    

def driveRover(dir):
    if (dir in MotorCom.direction):
        MotorCom.send_command(ser, MotorCom.direction[dir])
        MotorCom.receive_from_arduino(ser)
    else:
        print("[WARNING] NOT VALID DIRECTION")    

def turnRover(turnDir):
    if (turnDir in MotorCom.direction):    
        MotorCom.send_command(SERIAL_PORT, MotorCom.turnDirection[turnDir])
        time.sleep(1)   #Time it takes to turn 90 in a direction
        MotorCom.send_command(SERIAL_PORT, MotorCom.turnDirection("STOP"))        
    else:
        print("[WARNING] NOT VALID TURN DIRECTION")    
       
def actuateArm(dir):
    if (dir in MotorCom.arm):
        MotorCom.send_command(SERIAL_PORT, MotorCom.arm[dir])
        time.sleep(1)   #Time it takes to complete arm movement
        MotorCom.send_command(SERIAL_PORT, MotorCom.arm("STOP"))     
    else:
        print("[WARNING] NOT VALID ARM MOVEMENT")    
        
def toggleVibration(tog):
    if (tog in MotorCom.vibration):
        MotorCom.send_command(SERIAL_PORT, MotorCom.vibration[tog])      
    else:
        print("[WARNING] NOT VALID VIBRATION TOGGLE")    

def calculateDistanceTraveled(startCoords, currentCoords):
    #code to measure how far the rover moved from position
    distance = 0 #calculated from IMU and GPS
    return distance

def roverTravelDistance(targetDistance):
    distance = 0
    while (distance < targetDistance):
        distance = calculateDistanceTraveled()
        time.sleep(0.1)
        
def driveRoverDistance(dir, dist):
    driveRover(dir)
    distanceTraveled = 0
    #set to gps coord
    # startCoord = 0
    roverTravelDistance(dist)
    driveRover("STOP")

def stopRover():
    #tell ardrino to stop all function
    MotorCom.send_command(SERIAL_PORT, MotorCom.STOP)
    MotorCom.receive_from_arduino(ser)
    return None

def rerouteRover():
    #reroute rover around an obstacle    
    #backward
    #stop vibration
    #raise arm
    #turn rover 90 degrees left
    #forward
    #90 right
    #forward
    #90 right
    #try forward else repeat
    #90 left
    
    driveRoverDistance("BACKWARD", ROVER_LENGTH / 2)
    toggleVibration("OFF")
    actuateArm("UP")
    turnRover("LEFT")
    driveRoverDistance("FORWARD", ROVER_WIDTH)
    turnRover("RIGHT")
    driveRoverDistance("FORWARD", ROVER_LENGTH)
    turnRover("RIGHT")
    driveRoverDistance("FORWARD", ROVER_LENGTH / 2)    
    if (ForceButton.GetForceButton()):
        rerouteRover()
    else:
        turnRover("LEFT")

def roverClearArea(lineLength, numLines):
    finishedLine = False
    finishedGrid = False
    turnRight = True        #True = Right Turn, 
                            #False = Left Turn
    numLinesCompleted = 0
    distanceTraveled = 0
    pathObstructed = False
    
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            while not finishedGrid:
                #start of new line
                driveRover("FORWARD")   #drive rover forward
                while not finishedLine:
                    pathObstructed = ForceButton.GetForceButton()                    
                    if (pathObstructed):
                        rerouteRover()
                    
                    distanceTraveled = calculateDistanceTraveled()
                    if distanceTraveled >= lineLength: #meters
                        finishedLine = True
                        
                    time.sleep(0.1)
                        
                if (turnRight):
                    turnRover("RIGHT")
                    turnRight = False
                else:
                    turnRover("LEFT")
                    turnRight = True
                    
                numLinesCompleted += 1
                
                if (numLinesCompleted < numLines):
                    finishedGrid = False
                else:
                    finishedGrid = True
                    
                time.sleep(0.1)
            stopRover()
            
    except serial.SerialException as e:
        print("[ERROR] Serial communication issue:", e)
            
            
def main():        
    #Must send dummy command to wait for rover to be ready!!!
    driveRover("STOP")
    
    #Begin actual pathing
    driveRover("FORWARD")
    time.sleep(5)
    driveRover("BACKWARD")
    time.sleep(5)
    driveRover("STOP")
    
    
if __name__ == "__main__":
    main()

