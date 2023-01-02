import RPi.GPIO as GPIO


class Wheel:
    def __init__(self, port_1: int, port_2: int) -> None:
        for port in (port_1, port_2):
            GPIO.setup(port, GPIO.OUT)
            GPIO.output(port, GPIO.LOW)
        self.port_1_pwm = GPIO.PWM(port_1, 9600)
        self.port_1_pwm.start(0)
        self.port_2_pwm = GPIO.PWM(port_2, 9600)
        self.port_2_pwm.start(0)

    def move(self, speed: float) -> None:
        # Bound speed to be -1 <= speed <= 1
        speed = min(max(speed, -1), 1)

        # Determine individual pin duty cycles
        self.port_1_pwm.ChangeDutyCycle(50 * (speed+1))
        self.port_2_pwm.ChangeDutyCycle(100 - 50 * (speed+1))
