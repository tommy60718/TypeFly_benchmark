# TypeFly_benchmark/setup_env.sh
#!/bin/bash

# Create conda environment
conda create -n typefly python=3.10 -y

# Activate environment
conda activate typefly

# Install PyTorch with conda (for M2 optimization)
pip3 install --pre torch torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# Install other dependencies
pip install -r requirements.txt

# Generate proto files
cd proto && bash generate.sh

# Set environment variables
echo "export OPENAI_API_KEY=your_api_key_here" >> ~/.bashrc