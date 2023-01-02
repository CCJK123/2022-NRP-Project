import asyncio
import time

import RPi.GPIO as GPIO


class Pin():
    def __init__(self, port_no: int) -> None:
        self.port_no = port_no
        GPIO.setup(port_no, GPIO.OUT)
        GPIO.output(port_no, GPIO.LOW)


class PWM(Pin):
    def __init__(self, port_no: int, frequency: int) -> None:
        super().__init__()
        self.port_no = port_no
        self.frequency = frequency

    async def run(self, duty_cycle: float, duration_sec: float):
        # Bound duty_cycle within 0 <= duty_cycle <= 1
        duty_cycle = min(max(duty_cycle, 0), 1)

        # Software PWM
        # # Setup
        start_time = time.time()
        duration_high_sec = duty_cycle / self.frequency
        duration_low_sec = (1 - duty_cycle) / self.frequency

        # # Actual PWM
        while (time.time() - start_time) <= duration_sec:
            GPIO.output(self.port_no, GPIO.HIGH)
            await asyncio.sleep(duration_high_sec)
            GPIO.output(self.port_no, GPIO.LOW)
            await asyncio.sleep(duration_low_sec)


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


async def main():
    GPIO.setmode(GPIO.BOARD)

    front_left_wheel = Wheel(29, 31)

    for speed in range(1, -1.5, -0.5):
        await front_left_wheel.move(speed, 3)


if __name__ == "__main__":
    # For Python 3.7+
    # asyncio.run(main())

    # For Python 3.5 to 3.6
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
