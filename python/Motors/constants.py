import time


# Number of motor steps in one 90° turn
NUM_STEPS = 400

# Delay between motor steps (microseconds)
# Do not go below 50!
STEP_DELAY = 50

# Converts seconds to microseconds
MICRO_SLEEP = lambda t: time.sleep(t/1_000_000)

# Enable pin (common to all motor drivers)
ENABLE_PIN = 21

F_MOTOR_STEP_PIN = 6
F_MOTOR_DIR_PIN  = 5

B_MOTOR_STEP_PIN = 22
B_MOTOR_DIR_PIN  = 23

L_MOTOR_STEP_PIN = 25
L_MOTOR_DIR_PIN  = 24

R_MOTOR_STEP_PIN = 27
R_MOTOR_DIR_PIN  = 17

D_MOTOR_STEP_PIN = 16
D_MOTOR_DIR_PIN  = 26

PIN_DICT = {
    'F': (F_MOTOR_STEP_PIN, F_MOTOR_DIR_PIN),
    'B': (B_MOTOR_STEP_PIN, B_MOTOR_DIR_PIN),
    'L': (L_MOTOR_STEP_PIN, L_MOTOR_DIR_PIN),
    'R': (R_MOTOR_STEP_PIN, R_MOTOR_DIR_PIN),
    'D': (D_MOTOR_STEP_PIN, D_MOTOR_DIR_PIN)
}
