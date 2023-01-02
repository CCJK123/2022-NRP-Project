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
        super().__init__(port_no)
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
