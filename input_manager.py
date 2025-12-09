import time
import board
import digitalio
import busio
import math
import adafruit_adxl34x
from rotary_encoder import RotaryEncoder
import adafruit_adxl34x

class KnobController:
    def __init__(self, pin_a=board.D1, pin_b=board.D2, pin_button=board.D0,
                 encoder_cd=0.3, debounce_ms=3, pulses_per_detent=3):

        # Rotary encoder
        self.encoder = RotaryEncoder(pin_a, pin_b,
                                     debounce_ms=debounce_ms,
                                     pulses_per_detent=pulses_per_detent)

        # Button input
        self.button = digitalio.DigitalInOut(pin_button)
        self.button.switch_to_input(pull=digitalio.Pull.UP)

        self.encoder_cd = encoder_cd  # cd
        self._last_encoder_time = 0
        self._last_button_state = self.button.value
        self._last_button_time = 0
        self.button_cd = 0.3  

    def check(self):
        """
        return:
            ("turn", +1 / -1)
            ("press", None)

        """
        now = time.monotonic()

        # --- 1. check rotary ---
        changed = self.encoder.update()
        if changed and (now - self._last_encoder_time) > self.encoder_cd:
            delta = self.encoder.get_delta()
            if delta != 0:
                self._last_encoder_time = now
                if delta > 0:
                    return ("turn", +1)
                else:
                    return ("turn", -1)

        # --- 2. check btn ---
        current_button = self.button.value
        if current_button != self._last_button_state:
            self._last_button_time = now
            self._last_button_state = current_button

        
        if not current_button: 
            if now - self._last_button_time > self.button_cd:
                return ("press", None)

        return None


class Accelerator:

    def __init__(self,
                 accel_device,
                 tilt_threshold=2.2,
                 lane_cd=1.0,
                 shake_delta=2.5,
                 shake_frames=2,
                 alpha=0.2):

        self.accel = accel_device

        # EMA
        self.alpha = alpha
        self.fx = self.fy = self.fz = 0
        self.previous_fx = self.previous_fy = self.previous_fz = 0

        # threshold
        self.tilt_threshold = tilt_threshold
        self.shake_delta = shake_delta
        self.shake_frames = shake_frames

        # shake counter
        self.shake_counter = 0

        # CD
        self.lane_cd = lane_cd
        self.last_lane_change = time.monotonic()

        # baseline calibration
        self.baseline_x, self.baseline_y, self.baseline_z = self._calibrate()

    # -------------------------------------------------
    # calibrate baseline
    # -------------------------------------------------
    def _calibrate(self, samples=30):
        sum_x = sum_y = sum_z = 0
        for _ in range(samples):
            x, y, z = self.accel.acceleration
            sum_x += x
            sum_y += y
            sum_z += z
            time.sleep(0.05)
        return sum_x / samples, sum_y / samples, sum_z / samples

    # -------------------------------------------------
    # update
    # -------------------------------------------------
    def update(self):
        """
        return (left, right, shake)
        """

        left = right = shake = False

        # -------------------------
        # read
        # -------------------------
        raw_x, raw_y, raw_z = self.accel.acceleration
        x = raw_x - self.baseline_x
        y = raw_y - self.baseline_y
        z = raw_z - self.baseline_z

        # EMA
        self.fx = self.alpha * x + (1 - self.alpha) * self.fx
        self.fy = self.alpha * y + (1 - self.alpha) * self.fy
        self.fz = self.alpha * z + (1 - self.alpha) * self.fz

        # -------------------------
        # shake
        # -------------------------
        dx = abs(self.fx - self.previous_fx)
        dy = abs(self.fy - self.previous_fy)
        dz = abs(self.fz - self.previous_fz)
        delta = max(dx, dy, dz)

        if delta > self.shake_delta:
            self.shake_counter += 1
        else:
            self.shake_counter = 0

        # update to current
        self.previous_fx = self.fx
        self.previous_fy = self.fy
        self.previous_fz = self.fz

        # -------------------------
        # shake
        # -------------------------
        if self.shake_counter >= self.shake_frames:
            shake = True
            self.shake_counter = 0
            print("SHAKE")
            return left, right, shake

        # -------------------------
        # left/right
        # -------------------------
        t = time.monotonic()

        if self.fx > self.tilt_threshold and (t - self.last_lane_change) > self.lane_cd:
            right = True
            self.last_lane_change = t
            print("RIGHT")

        elif self.fx < -self.tilt_threshold and (t - self.last_lane_change) > self.lane_cd:
            left = True
            self.last_lane_change = t
            print("LEFT")

        return left, right, shake


