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

    def move_directional(self, angle_deg: float, speed: float) -> None:
        # Bound angle_deg to be 0 <= angle <= 360
        angle_deg = angle_deg % 360

        # Bound speed to be -1 <= speed <= 1
        speed = min(max(speed, -1), 1)

        # Determine individual wheel movement
        if 0 <= angle_deg < 90:
            self.front_left_wheel.move(speed)
            self.front_right_wheel.move(speed * (45-angle_deg)/45)
            self.back_left_wheel.move(speed * (45-angle_deg)/45)
            self.back_right_wheel.move(speed)
        elif 90 <= angle_deg < 180:
            self.front_left_wheel.move(speed * (135-angle_deg)/45)
            self.front_right_wheel.move(-speed)
            self.back_left_wheel.move(-speed)
            self.back_right_wheel.move(speed * (135-angle_deg)/45)
        elif 180 <= angle_deg < 270:
            self.front_left_wheel.move(-speed)
            self.front_right_wheel.move(speed * (angle_deg-225)/45)
            self.back_left_wheel.move(speed * (angle_deg-225)/45)
            self.back_right_wheel.move(-speed)
        else:  # 270 <= angle_deg <= 360
            self.front_left_wheel.move(speed * (angle_deg-315)/45)
            self.front_right_wheel.move(speed)
            self.back_left_wheel.move(speed)
            self.back_right_wheel.move(speed * (angle_deg-315)/45)

    def move_rotate_center(self, rotation_rate: float) -> None:
        # Take clockwise as positive rotation_rate

        # Bound rotation_rate to be -1 <= rotation_rate <= 1
        rotation_rate = min(max(rotation_rate, -1), 1)

        # Determine individual wheel movement
        self.front_left_wheel.move(rotation_rate)
        self.front_right_wheel.move(-rotation_rate)
        self.back_left_wheel.move(rotation_rate)
        self.back_right_wheel.move(-rotation_rate)

    def move_rotate_rear(self, rotation_rate: float) -> None:
        self.front_left_wheel.move(rotation_rate)
        self.front_right_wheel.move(-rotation_rate)
        self.back_left_wheel.move(0)
        self.back_left_wheel.move(0)
