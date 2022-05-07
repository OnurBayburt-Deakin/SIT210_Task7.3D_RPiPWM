#Import modules
import RPi.GPIO as GPIO
import time
from math import sqrt

#Initialise variables and setup pins
TRIG = 11
ECHO = 13
BUZZ = 12
SPEED = 17150
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(BUZZ,GPIO.OUT)
pwm = GPIO.PWM(BUZZ,2000)  #Buzzer's base frequency set to 2000Hz
pwm.start(0)  #Buzzer starts with duty cycle set to 0

#Calculate object distance from ultrasonic sensor
def distance():
    startTime = time.time()
    stopTime = time.time()

    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(TRIG, GPIO.LOW)
    
    while GPIO.input(ECHO) == 0:
        startTime = time.time()
    
    while GPIO.input(ECHO) == 1:
        stopTime = time.time()
        
    duration = stopTime - startTime
    distance = duration * SPEED
    return distance

#Activate buzzer with a variable frequency
def buzzer(pitch):
    pwm.ChangeFrequency(pitch)

#Main loop
try:
    while True:
        dist = distance()
        dist = int(dist)
        pitch = (1 / sqrt(dist)) * 2000
        
        if dist < 100:  #Object detection starts from 100cm away
            pwm.ChangeDutyCycle(50)  #Provide power to the buzzer
            buzzer(pitch)  #Alter buzzer pitch based on object distance
        else:
            pwm.ChangeDutyCycle(0)  #Power down the buzzer
except KeyboardInterrupt:  #Stop the program with a key press
    pwm.stop()
    GPIO.output(BUZZ,GPIO.LOW)
    GPIO.cleanup()
