import os
import base64
import logging
import webbrowser
from datetime import datetime
from pathlib import Path

# Set logging
logger = logging.getLogger(__name__)

def save_image(image_bytes: bytes, open_browser: bool = True, output_path: str = None) -> dict:
    """
    Save image to specified directory.
    
    Args:
        image_bytes (bytes): Image byte data
        open_browser (bool): Whether to open image in browser
        output_path (str): Optional specific path to save the image
        
    Returns:
        Dict: Image file path and data information
    """
    if output_path:
        filepath = output_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    else:
        # Set default save path to desktop
        desktop_path = Path.home() / 'Desktop' / 'aws-nova-canvas'
        # Create directory if it doesn't exist
        desktop_path.mkdir(parents=True, exist_ok=True)
        
        # Create unique file name using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.png"
        filepath = os.path.join(desktop_path, filename)
    
    # Save image to file
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    
    # Log file path
    logger.info(f"Image saved: {filepath}")
    
    # Encode generated image to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Open image in browser
    if open_browser:
        try:
            webbrowser.open(f"file://{filepath}")
            logger.info("Opened image in browser")
        except Exception as e:
            logger.warning(f"Failed to open image in browser: {e}")
    
    return {
        "image_path": filepath,
        "image_base64": image_base64,
        "filename": os.path.basename(filepath)
    } 