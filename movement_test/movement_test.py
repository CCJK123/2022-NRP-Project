import RPi.GPIO as GPIO
import time

# Setup connections
GPIO.setmode(GPIO.BOARD)
for port in (21, 22, 23, 24, 35, 36, 37, 38):
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, GPIO.LOW)

for i in range(10):
    GPIO.output(21, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(21, GPIO.LOW)

    GPIO.output(22, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(22, GPIO.LOW)

    GPIO.output(23, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(23, GPIO.LOW)

    GPIO.output(24, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(24, GPIO.LOW)

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

for port in (21, 22, 23, 24, 35, 36, 37, 38):
    GPIO.output(port, GPIO.LOW)

GPIO.cleanup()
