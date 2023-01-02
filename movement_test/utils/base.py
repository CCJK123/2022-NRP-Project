import asyncio

import RPi.GPIO as GPIO

from wheel import Wheel


class Base:
    def __init__(self,
                 front_left_wheel: Wheel, front_right_wheel: Wheel,
                 back_left_wheel: Wheel, back_right_wheel: Wheel
                 ) -> None:
        self.front_left_wheel = front_left_wheel
        self.front_right_wheel = front_right_wheel
        self.back_left_wheel = back_left_wheel
        self.back_right_wheel = back_right_wheel

    async def move_directional(self, angle_deg: float, speed: float, duration_sec: float) -> None:
        # Bound angle_deg to be 0 <= angle <= 360
        angle_deg = angle_deg % 360

        # Bound speed to be -1 <= speed <= 1
        speed = min(max(speed, -1), 1)

        # Determine individual wheel movement
        if 0 <= angle_deg < 90:
            tasks = [
                self.front_left_wheel.move(speed, duration_sec),
                self.front_right_wheel.move(
                    speed * (45-angle_deg)/45, duration_sec),
                self.back_left_wheel.move(
                    speed * (45-angle_deg)/45, duration_sec),
                self.back_right_wheel.move(speed, duration_sec)
            ]
        elif 90 <= angle_deg < 180:
            tasks = [
                self.front_left_wheel.move(
                    speed * (135-angle_deg)/45, duration_sec),
                self.front_right_wheel.move(-speed, duration_sec),
                self.back_left_wheel.move(-speed, duration_sec),
                self.back_right_wheel.move(
                    speed * (135-angle_deg)/45, duration_sec)
            ]
        elif 180 <= angle_deg < 270:
            tasks = [
                self.front_left_wheel.move(-speed, duration_sec),
                self.front_right_wheel.move(
                    speed * (angle_deg-225)/45, duration_sec),
                self.back_left_wheel.move(
                    speed * (angle_deg-225)/45, duration_sec),
                self.back_right_wheel.move(-speed, duration_sec)
            ]
        else:  # 270 <= angle_deg <= 360
            tasks = [
                self.front_left_wheel.move(
                    speed * (angle_deg-315)/45, duration_sec),
                self.front_right_wheel.move(speed, duration_sec),
                self.back_left_wheel.move(speed, duration_sec),
                self.back_right_wheel.move(
                    speed * (angle_deg-315)/45, duration_sec)
            ]
        await asyncio.wait([asyncio.ensure_future(task) for task in tasks])

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
