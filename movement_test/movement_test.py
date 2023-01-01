import RPi.GPIO as GPIO
import time

# Setup connections
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)  # IN 1
GPIO.setup(24, GPIO.OUT)  # IN 2
GPIO.setup(26, GPIO.OUT)  # IN 3
GPIO.setup(28, GPIO.OUT)  # IN 4

for i in range(10):
    GPIO.output(22, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(22, GPIO.LOW)

    GPIO.output(24, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(24, GPIO.LOW)

    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(26, GPIO.LOW)

    GPIO.output(28, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(28, GPIO.LOW)

GPIO.cleanup()
