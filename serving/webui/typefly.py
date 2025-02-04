import queue
import sys, os
import asyncio
import io, time
import gradio as gr
from flask import Flask, Response
from threading import Thread
import argparse

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(PARENT_DIR)
from controller.llm_controller import LLMController
from controller.utils import print_t
from controller.llm_wrapper import GPT4, LLAMA3
from controller.abs.robot_wrapper import RobotType

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class TypeFly:
    def __init__(self, robot_type, use_http=False):
         # create a cache folder
        self.cache_folder = os.path.join(CURRENT_DIR, 'cache')
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)
        self.message_queue = queue.Queue()
        self.message_queue.put(self.cache_folder)
        self.llm_controller = LLMController(robot_type, use_http, self.message_queue)
        self.system_stop = False
        self.ui = gr.Blocks(title="TypeFly")
        self.asyncio_loop = asyncio.get_event_loop()
        self.use_llama3 = False
        default_sentences = [
            "Find something I can eat.",
            "What you can see?",
            "Follow that ball for 20 seconds",
            "Find a chair for me.",
            "Go to the chair without book.",
        ]
        with self.ui:
            gr.HTML(open(os.path.join(CURRENT_DIR, 'header.html'), 'r').read())
            gr.HTML(open(os.path.join(CURRENT_DIR, 'drone-pov.html'), 'r').read())
            gr.ChatInterface(self.process_message,
                            retry_btn=None,
                            examples=default_sentences)
            # TODO: Add checkbox to switch between llama3 and gpt4
            # gr.Checkbox(label='Use llama3', value=False).select(self.checkbox_llama3)
            
            # Why: The error occurs because the yield in process_message 
            # requires queue functionality at the Blocks level, 
            # not just the ChatInterface level.
            self.ui.queue() #Move queue() here to fix the error

    def checkbox_llama3(self):
        self.use_llama3 = not self.use_llama3
        if self.use_llama3:
            print_t(f"Switch to llama3")
            self.llm_controller.planner.set_model(LLAMA3)
        else:
            print_t(f"Switch to gpt4")
            self.llm_controller.planner.set_model(GPT4)

    def process_message(self, message, history):
        print_t(f"[S] Receiving task description: {message}")
        if message == "exit":
            self.llm_controller.stop_controller()
            self.system_stop = True
            yield "Shutting down..."
        elif len(message) == 0:
            return "[WARNING] Empty command!]"
        else:
            # Thread 5: Task execution thread (created per command)
            # Handles: Individual command executino, plan interpretation
            task_thread = Thread(target=self.llm_controller.execute_task_description, args=(message,))
            task_thread.start()
            complete_response = ''
            while True:
                msg = self.message_queue.get()
                if isinstance(msg, tuple):
                    # history.append((message, complete_response))
                    history.append((None, msg))
                    # complete_response = ''
                elif isinstance(msg, str):
                    if msg == 'end':
                        # Indicate end of the task to Gradio chat
                        return "Command Complete!"
                    
                    if msg.startswith('[LOG]'):
                        complete_response += '\n'
                    if msg.endswith('\\\\'):
                        complete_response += msg.rstrip('\\\\')
                    else:
                        complete_response += msg + '\n'
                yield complete_response

    def generate_mjpeg_stream(self):
        while True:
            if self.system_stop:
                break
            frame = self.llm_controller.get_latest_frame(True)
            if frame is None:
                continue
            buf = io.BytesIO()
            frame.save(buf, format='JPEG')
            buf.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf.read() + b'\r\n')
            time.sleep(1.0 / 30.0)

    def run(self):
        # Thread 1: Asyncio Loop Thread
        asyncio_thread = Thread(target=self.asyncio_loop.run_forever)
        asyncio_thread.start()
        # Handles: Asynchronous operations, network communication, gRPC calls
        # See notion for more details

        # Thread 2: LLM controller thread
        # Handles: Frame capture, YOLO detection, LLM planning, robot control
        self.llm_controller.start_robot()
        llmc_thread = Thread(target=self.llm_controller.capture_loop, args=(self.asyncio_loop,))
        llmc_thread.start()


        # Set up Flask server for video streaming
        app = Flask(__name__)
        @app.route('/drone-pov/')
        def video_feed():
            return Response(self.generate_mjpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        # Thread 3: Flask server thread
        # Handles: streaming video to web UI
        # Debug mode enabled
        # Reload disabled to prevent duplicate processes
        flask_thread = Thread(target=app.run,
                             kwargs={'host': 'localhost',
                                     'port': 50000,
                                     'debug': True, 
                                     'use_reloader': False})
        flask_thread.start()

        # Thread 4: Gradio UI thread
        # Handles: Web UI, chat interface, user interactions
        self.ui.launch(show_api=False, server_port=50001, prevent_thread_lock=True, share=True)

        # Main monitoring loop
        # Check system_stop flag every second for graceful shutdown
        while True:
            time.sleep(1)
            if self.system_stop:
                break

        # Join threads to ensure clean termination  
        llmc_thread.join()
        asyncio_thread.join()

        #Shutdown robot systems
        self.llm_controller.stop_robot()

        # Remove all temporary files from cache folder
        for file in os.listdir(self.cache_folder):
            os.remove(os.path.join(self.cache_folder, file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--use_virtual_robot', action='store_true')
    parser.add_argument('--use_http', action='store_true')
    parser.add_argument('--gear', action='store_true')
    parser.add_argument('--use_simulator', action='store_true', help='Use simulator mode for drone control')

    args = parser.parse_args()
    robot_type = RobotType.TELLO
    if args.use_virtual_robot:
        robot_type = RobotType.VIRTUAL
    elif args.gear:
        robot_type = RobotType.GEAR
    elif args.use_simulator:
        robot_type = RobotType.SIMULATOR
    typefly = TypeFly(robot_type, use_http=args.use_http)
    typefly.run()