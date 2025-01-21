#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p netlify/functions

# Copy Streamlit files to publish directory
cp -r streamlit_frontend/* netlify/functions/

# Make the script executable
chmod +x build.sh 