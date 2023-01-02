from utils.wheel import Wheel
from utils.base import Base

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

front_left_wheel = Wheel(29, 31)
front_right_wheel = Wheel(32, 33)
back_left_wheel = Wheel(35, 36)
back_right_wheel = Wheel(37, 38)
wheel_base = Base(front_left_wheel, front_right_wheel,
                  back_left_wheel, back_right_wheel)

for speed in (1, 0.5, -0.5, -1, 0):
    for angle_deg in range(360):
        wheel_base.move_directional(angle_deg, speed)
        time.sleep(0.1)
    time.sleep(5)
