import sys
import os
import cv2
import time
from PIL import Image

# Add the parent directory to the Python path
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

from controller.simulator_wrapper import SimulatorWrapper

def test_frame_capture():
    print("Starting simulator frame capture test...")
    
    # Initialize simulator
    simulator = SimulatorWrapper()
    simulator.connect()
    simulator.takeoff()
    
    # Start streaming
    print("Starting stream...")
    success = simulator.start_stream()
    if not success:
        print("Failed to start stream!")
        return
    
    # Get frame reader
    frame_reader = simulator.get_frame_reader()
    if frame_reader is None:
        print("Failed to get frame reader!")
        return
    
    # Capture and display frames
    try:
        for i in range(50):  # Test 50 frames
            frame = frame_reader.frame
            if frame is None:
                print(f"Frame {i}: No frame captured!")
                continue
                
            # Print frame info
            print(f"Frame {i}: Shape={frame.shape}, Type={frame.dtype}")
            
            # Convert to PIL Image for display
            pil_image = Image.fromarray(frame)
            
            # Save a few sample frames
            if i % 10 == 0:
                save_path = os.path.join(PARENT_DIR, f"test/frame_{i}.jpg")
                pil_image.save(save_path)
                print(f"Saved frame to {save_path}")
            
            time.sleep(0.1)  # 10 FPS
            
    except Exception as e:
        print(f"Error during capture: {e}")
    finally:
        # Cleanup
        simulator.stop_stream()
        print("Test completed.")

if __name__ == "__main__":
    test_frame_capture()