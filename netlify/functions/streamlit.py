from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os

def handler(event, context):
    # Set environment variables
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    
    try:
        # Start Streamlit process
        process = subprocess.Popen(
            ['streamlit', 'run', 'streamlit_frontend/Home.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': '<html><body><h1>Streamlit app is running!</h1></body></html>'
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'body': str(e)
        } 