import RPi.GPIO as GPIO
import time

# Setup connections
GPIO.setmode(GPIO.BOARD)
for port in (29, 31, 32, 33, 35, 36, 37, 38):
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, GPIO.LOW)

for i in range(10):
    GPIO.output(29, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(29, GPIO.LOW)

    GPIO.output(31, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(31, GPIO.LOW)

    GPIO.output(32, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(32, GPIO.LOW)

    GPIO.output(33, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(33, GPIO.LOW)

    GPIO.output(35, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(35, GPIO.LOW)

    GPIO.output(36, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(36, GPIO.LOW)

    GPIO.output(37, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(37, GPIO.LOW)

    GPIO.output(38, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(38, GPIO.LOW)

for port in (29, 31, 32, 33, 35, 36, 37, 38):
    GPIO.output(port, GPIO.LOW)

GPIO.cleanup()
