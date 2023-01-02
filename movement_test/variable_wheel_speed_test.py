import asyncio

import RPi.GPIO as GPIO

from utils.wheel import Wheel


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
