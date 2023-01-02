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
        if speed >= 0:
            await self.port_1_pwm.run(speed, duration_sec)
        else:
            await self.port_2_pwm.run(-speed, duration_sec)


class Base:
    def __init__(self,
                 front_left_wheel: Wheel, front_right_wheel: Wheel,
                 back_left_wheel: Wheel, back_right_wheel: Wheel
                 ) -> None:
        self.front_left_wheel = front_left_wheel
        self.front_right_wheel = front_right_wheel
        self.back_left_wheel = back_left_wheel
        self.back_right_wheel = back_right_wheel

    def move_directional(self, angle_deg: float, speed: float, duration_sec: float) -> None:
        # Bound angle_deg to be 0 <= angle <= 360
        angle_deg = angle_deg % 360

        # Bound speed to be -1 <= speed <= 1
        speed = min(max(speed, -1), 1)

        # Determine individual wheel movement
        if 0 <= angle_deg < 90:
            self.front_left_wheel.move(speed, duration_sec)
            self.front_right_wheel.move(
                speed * (45-angle_deg)/45, duration_sec)
            self.back_left_wheel.move(speed * (45-angle_deg)/45, duration_sec)
            self.back_right_wheel.move(speed, duration_sec)
        elif 90 <= angle_deg < 180:
            self.front_left_wheel.move(
                speed * (135-angle_deg)/45, duration_sec)
            self.front_right_wheel.move(-speed, duration_sec)
            self.back_left_wheel.move(-speed, duration_sec)
            self.back_right_wheel.move(
                speed * (135-angle_deg)/45, duration_sec)
        elif 180 <= angle_deg < 270:
            self.front_left_wheel.move(-speed, duration_sec)
            self.front_right_wheel.move(
                speed * (angle_deg-225)/45, duration_sec)
            self.back_left_wheel.move(speed * (angle_deg-225)/45, duration_sec)
            self.back_right_wheel.move(-speed, duration_sec)
        else:  # 270 <= angle_deg <= 360
            self.front_left_wheel.move(
                speed * (angle_deg-315)/45, duration_sec)
            self.front_right_wheel.move(speed, duration_sec)
            self.back_left_wheel.move(speed, duration_sec)
            self.back_right_wheel.move(
                speed * (angle_deg-315)/45, duration_sec)

    def move_rotate_center(self, rotation_rate: float, duration_sec: float) -> None:
        # Take clockwise as positive rotation_rate

        # Bound rotation_rate to be -1 <= rotation_rate <= 1
        rotation_rate = min(max(rotation_rate, -1), 1)

        # Determine individual wheel movement
        self.front_left_wheel.move(rotation_rate, duration_sec)
        self.front_right_wheel.move(-rotation_rate, duration_sec)
        self.back_left_wheel.move(rotation_rate, duration_sec)
        self.back_right_wheel.move(-rotation_rate, duration_sec)

    def move_rotate_rear(self, rotation_rate: float, duration_sec) -> None:
        self.front_left_wheel.move(rotation_rate, duration_sec)
        self.front_right_wheel.move(-rotation_rate, duration_sec)
        self.back_left_wheel.move(0, duration_sec)
        self.back_left_wheel.move(0, duration_sec)


async def main():
    GPIO.setmode(GPIO.BOARD)

    front_left_wheel = Wheel(29, 31)
    front_right_wheel = Wheel(32, 33)
    back_left_wheel = Wheel(35, 36)
    back_right_wheel = Wheel(37, 38)
    wheel_base = Base(front_left_wheel, front_right_wheel,
                      back_left_wheel, back_right_wheel)

    for speed in (1, 0.5, -0.5, -1, 0):
        for angle_deg in range(360):
            await wheel_base.move_directional(angle_deg, speed, 0.1)
        await asyncio.sleep(5)


if __name__ == "__main__":
    # For Python 3.7+
    # asyncio.run(main())

    # For Python 3.5 to 3.6
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
