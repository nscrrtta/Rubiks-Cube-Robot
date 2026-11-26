from constants import *
import RPi.GPIO as GPIO
import zmq


class Motors:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect('tcp://localhost:5555')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENABLE_PIN, GPIO.OUT)
        for step_pin, dir_pin in PIN_DICT.values():
            GPIO.setup(step_pin, GPIO.OUT)
            GPIO.setup(dir_pin, GPIO.OUT)

        self._set_enable_pin(1)

    def wait_for_messages(self):
        while True:
            msg: dict = self.socket.recv_pyobj()
            if 'pin_state' in msg:
                self._set_enable_pin(msg['pin_state'])
            elif 'moves' in msg:
                self._make_moves(*msg['moves'])
            elif 'quit' in msg:
                break

    def _make_moves(self, f1: str, n1: int, f2: str, n2: int):
        # Move 1 values
        self._set_direction_pin(f1, n1)
        steps_i = self._get_num_steps(n1)
        step_pin_i = self._get_step_pin(f1)

        # Move 2 values
        self._set_direction_pin(f2, n2)
        steps_j = self._get_num_steps(n2)
        step_pin_j = self._get_step_pin(f2)

        while steps_i or steps_j:
            if steps_i:
                GPIO.output(step_pin_i, 1)
            if steps_j:
                GPIO.output(step_pin_j, 1)

            MICRO_SLEEP(STEP_DELAY)

            if steps_i:
                steps_i -= 1
                GPIO.output(step_pin_i, 0)

            if steps_j:
                steps_j -= 1
                GPIO.output(step_pin_j, 0)

            MICRO_SLEEP(STEP_DELAY)

    def _set_enable_pin(self, state: int):
        """Enable pin must be low for motors to turn."""
        GPIO.output(ENABLE_PIN, state)

    def _set_direction_pin(self, face: str, turns: int):
        if face not in PIN_DICT:
            return
        _, direction_pin = PIN_DICT[face]
        pin_val = 1 if turns == 3 else 0
        GPIO.output(direction_pin, pin_val)

    def _get_step_pin(self, face: str) -> int:
        if face not in PIN_DICT:
            return 0
        step_pin, _ = PIN_DICT[face]
        return step_pin

    def _get_num_steps(self, turns: int) -> int:
        return NUM_STEPS if turns % 2 else NUM_STEPS * turns


if __name__ == '__main__':
    motors = Motors()
    try:
        motors.wait_for_messages()
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
