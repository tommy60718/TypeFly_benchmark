import time
import cv2
import numpy as np
import mss
from typing import Tuple
from pynput.keyboard import Key, Controller
import threading
import queue

from .abs.robot_wrapper import RobotWrapper

MOVEMENT_MIN = 20
MOVEMENT_MAX = 300

SCENE_CHANGE_DISTANCE = 120
SCENE_CHANGE_ANGLE = 90

class FrameReader:
    def __init__(self, monitor_id=2):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_id]

    @property
    def frame(self):
        # Capture the screen
        screenshot = self.sct.grab(self.monitor)
        # Convert to numpy array and RGB format
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        return frame

class KeyboardController:
    def __init__(self):
        self.keyboard = Controller()
        self.action_queue = queue.Queue()
        self.running = True
        self.keyboard_thread = threading.Thread(target=self._keyboard_control_loop)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()

    def _keyboard_control_loop(self):
        while self.running:
            try:
                action = self.action_queue.get(timeout=0.1)
                if action:
                    self._execute_action(action)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Keyboard control error: {e}")

    def _execute_action(self, action_tuple):
        action, duration_ms = action_tuple
        key = self.action_map.get(action)
        if key:
            try:
                self.keyboard.press(key)
                time.sleep(duration_ms / 1000.0)
                self.keyboard.release(key)
                time.sleep(0.1)
            except Exception as e:
                print(f"Keyboard action failed: {e}")
                self.keyboard.release(key)

    def execute_action(self, action_tuple):
        self.action_queue.put(action_tuple)

    def stop(self):
        self.running = False
        if hasattr(self, 'keyboard_thread'):
            self.keyboard_thread.join()

    action_map = {
        'increase_throttle': 'w',
        'decrease_throttle': 's',
        'yaw_left': 'a',
        'yaw_right': 'd',
        'roll_left': Key.left,
        'roll_right': Key.right,
        'pitch_forward': Key.up,
        'pitch_back': Key.down
    }

def cap_distance(distance):
    if distance < MOVEMENT_MIN:
        return MOVEMENT_MIN
    elif distance > MOVEMENT_MAX:
        return MOVEMENT_MAX
    return distance

class SimulatorWrapper(RobotWrapper):
    def __init__(self):
        self.stream_on = False
        self.keyboard_controller = KeyboardController()
        self.movement_x_accumulator = 0
        self.movement_y_accumulator = 0
        self.rotation_accumulator = 0

    def keep_active(self):
        pass

    def connect(self):
        pass

    def takeoff(self) -> bool:
        return True

    def land(self):
        pass

    def start_stream(self):
        self.frame_reader = FrameReader()
        self.stream_on = True
        return True

    def stop_stream(self):
        self.stream_on = False
        self.keyboard_controller.stop()

    def get_frame_reader(self):
        if not self.stream_on:
            return None
        return self.frame_reader

    def move_forward(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('pitch_forward', distance))
        self.movement_x_accumulator += distance
        time.sleep(0.5)
        return True, distance > SCENE_CHANGE_DISTANCE

    def move_backward(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('pitch_back', distance))
        self.movement_x_accumulator -= distance
        time.sleep(0.5)
        return True, distance > SCENE_CHANGE_DISTANCE

    def move_left(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('roll_left', distance))
        self.movement_y_accumulator += distance
        time.sleep(0.5)
        return True, distance > SCENE_CHANGE_DISTANCE

    def move_right(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('roll_right', distance))
        self.movement_y_accumulator -= distance
        time.sleep(0.5)
        return True, distance > SCENE_CHANGE_DISTANCE

    def move_up(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('increase_throttle', distance))
        time.sleep(0.5)
        return True, False

    def move_down(self, distance: int) -> Tuple[bool, bool]:
        distance = cap_distance(distance)
        self.keyboard_controller.execute_action(('decrease_throttle', distance))
        time.sleep(0.5)
        return True, False

    def turn_ccw(self, degree: int) -> Tuple[bool, bool]:
        self.keyboard_controller.execute_action(('yaw_left', degree * 10))
        self.rotation_accumulator += degree
        time.sleep(1)
        return True, degree > SCENE_CHANGE_ANGLE

    def turn_cw(self, degree: int) -> Tuple[bool, bool]:
        self.keyboard_controller.execute_action(('yaw_right', degree * 10))
        self.rotation_accumulator -= degree
        time.sleep(1)
        return True, degree > SCENE_CHANGE_ANGLE 