import os
from dotenv import load_dotenv

def get_app_config():
    """Get application configurations from environment variables."""
    config = {
        'model_id': os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-canvas-v1:0'),
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
        'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
        'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'profile': os.environ.get('AWS_PROFILE'),
        'port': os.environ.get('PORT', '9527')
    }
    
    # If AWS credentials are not set, load from .env file
    if not (config['profile'] or (config['access_key'] and config['secret_key'])):
        print("AWS credentials are not set. Loading from .env file.")
        load_dotenv()
        config = {
            'model_id': os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-canvas-v1:0'),
            'region': os.environ.get('AWS_REGION', 'us-east-1'),
            'access_key': os.environ.get('AWS_ACCESS_KEY_ID'),
            'secret_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'profile': os.environ.get('AWS_PROFILE'),
            'port': os.environ.get('PORT', '9527')
        }
        
        # Check if either profile or access_key/secret_key pair is set
        has_profile = bool(config['profile'])
        has_keys = bool(config['access_key'] and config['secret_key'])
        
        if not (has_profile or has_keys):
            print("AWS credentials are not properly set. Either AWS_PROFILE or both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")
            
    return config 