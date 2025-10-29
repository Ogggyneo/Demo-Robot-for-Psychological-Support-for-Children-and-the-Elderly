import RPi.GPIO as GPIO
import time
import json
from gpiozero import DistanceSensor
from gpiozero import DigitalInputDevice
from gpiozero import Motor
from gpiozero import Servo


RIGHT = 17  
LEFT = 18   
TRIGGER_PIN = 23  
ECHO_PIN = 24     


right_ir = DigitalInputDevice(RIGHT)
left_ir = DigitalInputDevice(LEFT)
ultrasonic_sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIGGER_PIN)
motor1 = Motor(forward=27, backward=22) 
motor2 = Motor(forward=25, backward=12)  
motor3 = Motor(forward=5, backward=6)    
motor4 = Motor(forward=13, backward=19) 
servo = Servo(10)  

def move_forward(speed):
    motor1.forward(speed)
    motor2.forward(speed)
    motor3.forward(speed)
    motor4.forward(speed)

def turn_left(speed):
    motor1.forward(speed)
    motor2.forward(speed)
    motor3.backward(speed)
    motor4.backward(speed)
    time.sleep(0.15)

def turn_right(speed):
    motor1.backward(speed)
    motor2.backward(speed)
    motor3.forward(speed)
    motor4.forward(speed)
    time.sleep(0.15)

def stop_motors():
    motor1.stop()
    motor2.stop()
    motor3.stop()
    motor4.stop()


servo.mid()

try:
    while True:
        distance = ultrasonic_sensor.distance * 100  

        print("Distance:", distance)

        right_value = right_ir.value
        left_value = left_ir.value

        print("Right IR:", right_value)
        print("Left IR:", left_value)

        if distance < 15:
            move_forward(0.5)  
        elif right_value == 0 and left_value == 1:
            turn_left(0.6) 
        elif right_value == 1 and left_value == 0:
            turn_right(0.6)  
        else:
            stop_motors()

        time.sleep(0.1) 
finally:
    
    GPIO.cleanup()
