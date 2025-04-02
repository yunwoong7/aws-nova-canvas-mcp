import logging
from mcp import McpError

# Set logging
logger = logging.getLogger(__name__)

async def get_image(image_id: str) -> bytes:
    """
    Get an image by image ID.
    
    Args:
        image_id: Image ID
        
    Returns:
        bytes: Image data
    """
    try:
        # Here, we assume image_id is a file path.
        with open(image_id, "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Image load error: {e}")
        raise McpError(f"Unable to load image: {str(e)}") 