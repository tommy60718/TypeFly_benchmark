# TypeFly Simulator Mode Implementation V1

## Core Changes

### 1. Robot Wrapper Interface
- Added `SIMULATOR = 3` to `RobotType` enum in `controller/abs/robot_wrapper.py`
- Created `simulator_wrapper.py` implementing `RobotWrapper` interface

### 2. Screen Capture Implementation
```python
class FrameReader:
    def __init__(self, monitor_id=None):
        self.sct = mss.mss()
        # Use primary monitor by default
        self.monitor = self.sct.monitors[1]
        self.capture_region = {
            'top': self.monitor['top'],
            'left': self.monitor['left'],
            'width': self.monitor['width'],
            'height': self.monitor['height']
        }
```
- Uses `mss` library for efficient screen capture
- Converts frames to RGB format for YOLO processing

### 3. Keyboard Control
```python
class KeyboardController:
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
```
- Implements keyboard control using `pynput`
- Thread-safe action queue for smooth control


### 4. High-Level Skills
- Matched Tello's implementation exactly:
  - `scan`: Rotate to find objects
  - `scan_abstract`: Find abstract objects

- Copied and matched Tello's configuration structure:
  - `high_level_skills.json`: Basic scan and scan_abstract skills
  - `prompt_plan.txt`: LLM prompting template
  - `guides.txt`: Behavior guidelines
  - `plan_examples.txt`: Example commands and responses


### 5. Command Line Interface
Added simulator flag to `typefly.py`:
```python
parser.add_argument('--use_simulator', action='store_true', 
                   help='Use simulator mode for drone control')
```

## Dependencies Added
```
# requirements.txt
mss>=9.0.1  # Screen capture
pynput>=1.7.6  # Keyboard control
```

## macOS Specific Changes

### 1. Screen Capture
- Using `mss` library instead of `opencv` for better macOS compatibility
- Monitor selection defaults to primary display (index 1)

### 2. Keyboard Control
- Using `pynput` for cross-platform keyboard simulation
- Special handling for macOS keyboard permissions

### 3. Path Handling
- Using `os.path.join` for cross-platform path compatibility
- Absolute path handling for macOS directory structure

## Configuration Files

### 1. Assets Structure
```
controller/assets/simulator/
├── high_level_skills.json  # Matches Tello version
├── prompt_plan.txt         # Copied from Tello
├── prompt_probe.txt        # Copied from Tello
├── guides.txt             # Copied from Tello
└── plan_examples.txt      # Copied from Tello
```

### 2. Test Scripts
```
test/
└── test_simulator_capture.py  # Frame capture verification
```

## Linux to macOS Conversion Notes

### For Linux Version:
1. Screen Capture:
   - Replace `mss` with `opencv` if needed
   - Adjust monitor selection logic

2. Keyboard Control:
   - May use `xdotool` instead of `pynput`
   - Remove macOS-specific permission checks

3. Path Handling:
   - Update absolute paths to Linux format
   - Check file permissions

## Known Issues
1. Frame capture requires screen recording permissions on macOS
2. Keyboard control requires accessibility permissions on macOS
3. YOLO service connection handling needs improvement
4. Video streaming pipeline optimization needed

## Future Improvements
1. Better error handling for YOLO service connection
2. Improved frame capture region selection
3. More robust keyboard control error recovery
4. Enhanced cross-platform compatibility layer



## Error Handling(that I've fixed)
- Graceful handling of YOLO service failures
- Robust frame capture with error reporting
- Keyboard control error recovery

## Notes
1. Maintained exact compatibility with Tello's:
   - Same high-level skills structure
   - Same command interpretation
   - Same error handling patterns

2. Key Differences from Tello:
   - Uses screen capture instead of camera feed
   - Keyboard simulation instead of drone commands
   - Monitor selection for capture region

## Testing
Created test script `test_simulator_capture.py` to verify:
- Frame capture functionality
- Color space conversion
- Frame rate consistency

## Future Work
1. Monitor selection UI
2. Custom capture region support
3. Performance optimization for frame capture
4. Enhanced error reporting 