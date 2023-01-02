import RPi.GPIO as GPIO

from pin import PWM


class Wheel:
    def __init__(self, port_1: int, port_2: int) -> None:
        self.port_1_pwm = PWM(port_1, 9600)
        self.port_2_pwm = PWM(port_2, 9600)

    async def move(self, speed: float, duration_sec: float) -> None:
        # Bound speed to be -1 <= speed <= 1
        speed = min(max(speed, -1), 1)

        # Determine individual pin duty cycles
        await self.port_1_pwm.run(0.5*(speed+1), duration_sec)
        await self.port_2_pwm.run(1 - 0.5*(speed+1), duration_sec)
