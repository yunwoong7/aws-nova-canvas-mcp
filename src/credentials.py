import os
from pathlib import Path
from dotenv import load_dotenv

def get_aws_credentials():
    """Get AWS credentials from environment variables."""
    credentials = {
        'model_id': os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-canvas-v1:0'),
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
        'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
        'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'port': os.environ.get('PORT', '8000'),
        'images_dir': os.environ.get('IMAGES_DIR', os.path.join(str(Path.home()), 'nova_canvas_images'))
    }
    
    # If environment variables are not set, load from .env file
    if not all(credentials.values()):
        print("Environment variables are not set. Loading from .env file.")
        load_dotenv()
        credentials = {
            'model_id': os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-canvas-v1:0'),
            'region': os.environ.get('AWS_REGION', 'us-east-1'),
            'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
            'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'port': os.environ.get('PORT', '8000'),
            'images_dir': os.environ.get('IMAGES_DIR', os.path.join(str(Path.home()), 'nova_canvas_images'))
        }
        
        if not all(credentials.values()):
            raise ValueError("AWS credentials are not properly set.")
            
    return credentials 