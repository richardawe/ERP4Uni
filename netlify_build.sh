#!/bin/bash

# Exit on error
set -e

# Print commands
set -x

# Update pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Create Streamlit config
cat > .streamlit/config.toml << EOL
[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false
EOL

# Start Streamlit
streamlit run streamlit_frontend/Home.py 