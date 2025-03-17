# baisc rover path for 3x3 meter area
#   -moves forward 3 meters
#   -180 turn right with radius ~0.5m
#   -move forward 3 meters
#   -180 turn left with radius ~0.5m
#   -repeat until 6 passes

def driveRover(dir):
    #forward => dir = 1
    #back => dir = -1
    #stop => dir = 0
    #Code to drive rover
    
    if dir == 1:
        #tell ardrino to drive forward
    elif dir == -1:
        #tell ardrino to drive backward
    elif dir == 0:
        #tell ardrino to stop drive motors
    else:
        #tell ardrino to stop drive motors
    
    return None

def turnRover():
    #code to turn rover 180 degrees around a radius
    if turnDirection:
        #turn right
        
    else:
        #turn left
                
    return None

def stopRover():
    #tell ardrino to stop all function
    return None

def distanceTraveled():
    #code to measure how far the rover moved from position
    distance #calculated from IMU and GPS
    return distance

    
#main
finishedLine = False
finishedGrid = False
turnDirection = True    #True = Right Turn, 
                        #False = Left Turn
lineLength = 3
numLines = 6
numLinesCompleted = 0
                        
while not finishedGrid:
    driveRover(1)   #drive rover forward
    while not finishedLine:
        if distanceTraveled() >= lineLength: #meters
            finishedLine = True
            
    turnRover(turnDirection)
    turnDirection = not turnDirection
    numLinesCompleted += 1
    if (numLinesCompleted < numLines):
        finishedGrid = False
    else:
        finishedGrid = True

