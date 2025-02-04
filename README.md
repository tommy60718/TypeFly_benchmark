# TypeFly Benchmark

A benchmark system for testing natural language drone control, supporting multiple control modes including physical drones (Tello), virtual robots, and simulator environments.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start YOLO service (required for object detection):
```bash
make build SERVICE=yolo  # Build YOLO service container
make start SERVICE=yolo  # Start YOLO service
```

3. Run TypeFly in one of the following modes:

```bash
# Tello drone mode (default)
python -m serving.webui.typefly

# Virtual robot mode
python -m serving.webui.typefly --use_virtual_robot

# Simulator mode
python -m serving.webui.typefly --use_simulator

# Gear robot mode
python -m serving.webui.typefly --gear
```

## Modes

- **Tello Mode**: Controls physical Tello drones
- **Virtual Mode**: Simulated environment for testing without hardware
- **Simulator Mode**: Screen capture-based control for simulator environments
- **Gear Mode**: Controls Gear robot cars

## Features

- Natural language command processing
- Real-time object detection using YOLO
- Web-based control interface
- Multi-threaded architecture for responsive control
- High-level skill composition

## System Requirements

- Python 3.10+
- CUDA-capable GPU (recommended for YOLO service)
- Docker (for YOLO service)
- Screen capture capability (for simulator mode)

## Project Structure

```
TypeFly_benchmark/
├── controller/          # Core control logic
│   ├── assets/         # Mode-specific configurations
│   ├── abs/            # Abstract interfaces
│   └── simulator/      # Simulator mode implementation
├── serving/            # Web interface and services
├── test/              # Test scripts
└── docker/            # Docker configurations
```

## Common Commands

```bash
# Build and start YOLO service
make build SERVICE=yolo
make start SERVICE=yolo

# Stop services
make stop SERVICE=yolo

# Run tests
python -m test.test_simulator_capture  # Test simulator frame capture
```

## Notes

- YOLO service must be running for object detection
- Simulator mode requires proper screen capture permissions
- Web interface runs on ports 50000 (video stream) and 50001 (control interface)

## License

[Your License]
