# basic rover path for 3x3 meter area
#   -moves forward 3 meters
#   -180 turn right with radius ~0.5m
#   -move forward 3 meters
#   -180 turn left with radius ~0.5m
#   -repeat until 6 passes

import testmodule
import serial
import MotorCom

SERIAL_PORT = "/dev/ttyACM2"  # Update if necessary (e.g., "COM3" for Windows)
BAUD_RATE = 9600

def driveRover(dir):
    #forward => dir = 1
    #back => dir = -1
    #stop => dir = 0
    #Code to drive rover
    
    if dir == 1:
        #tell ardrino to drive forward
        print("Drive Forward")
        MotorCom.send_command(SERIAL_PORT, MotorCom.direction("FORWARD"))
    elif dir == -1:
        #tell ardrino to drive backward
        print("Drive Backward")
        MotorCom.send_command(SERIAL_PORT, MotorCom.direction("BACKWARD"))
    elif dir == 0:
        #tell ardrino to stop drive motors
        print("Stop")
        MotorCom.send_command(SERIAL_PORT, MotorCom.direction("STOP"))
    else:
        #tell ardrino to stop drive motors
        driveRover(0)
    
    return None

def turnRover(turnDir):
    #code to turn rover 180 degrees around a radius
    if turnDir:
        #turn right
        print("Turn Right")
        MotorCom.send_command(SERIAL_PORT, MotorCom.direction("RIGHT"))
    else:
        #turn left
        print("Turn Left")
        MotorCom.send_command(SERIAL_PORT, MotorCom.direction("LEFT"))
                
    return None

def stopRover():
    #tell ardrino to stop all function
    MotorCom.send_command(SERIAL_PORT, MotorCom.STOP)
    return None

def calculateDistanceTraveled(startCoords, currentCoords):
    #code to measure how far the rover moved from position
    distance = 0 #calculated from IMU and GPS
    return distance

def roverClearArea(lineLength, numLines):
    finishedLine = False
    finishedGrid = False
    turnDirection = True    #True = Right Turn, 
                            #False = Left Turn
    numLinesCompleted = 0
    distanceTraveled = 0
    
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            while not finishedGrid:
                #start of new line
                driveRover(1)   #drive rover forward
                while not finishedLine:
                    distanceTraveled = calculateDistanceTraveled()
                    if distanceTraveled >= lineLength: #meters
                        finishedLine = True
                        
                turnRover(turnDirection)
                turnDirection = not turnDirection
                numLinesCompleted += 1
                
                if (numLinesCompleted < numLines):
                    finishedGrid = False
                else:
                    finishedGrid = True
            stopRover()
            
    except serial.SerialException as e:
        print("[ERROR] Serial communication issue:", e)
            
            
def main():
    # roverClearArea(3, 6)
    pass
    
if __name__ == "__main__":
    main()

