import io
import requests
from PIL import Image as PILImage
from ..server import mcp, ImageError, McpError
from mcp.server.fastmcp import Image

@mcp.tool()
def show_image(image_path: str, width: int = 500, height: int = 500) -> Image:
    """
    Create a thumbnail of the image and return it. The maximum size is 1048578.
    Supports URLs or local file paths.
    
    Args:
        image_path: Image URL or local file path
        width: Output image width (pixels)
        height: Output image height (pixels)
        
    Returns:
        Image: Thumbnail image
    """
    try:
        # Check if image_path is a URL or local file path
        if image_path.startswith('http://') or image_path.startswith('https://'):
            # Download image from URL
            response = requests.get(image_path, stream=True)
            if response.status_code != 200:
                raise ImageError(f"Failed to download image: {response.status_code}")
            
            # Create image object
            img = PILImage.open(io.BytesIO(response.content))
        else:
            # Read local file
            try:
                img = PILImage.open(image_path)
            except FileNotFoundError:
                raise ImageError(f"Image file not found: {image_path}")
        
        # Create thumbnail
        img.thumbnail((width, height))
        
        # Convert RGBA image to RGB (if necessary)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Convert image to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        
        # Return image object
        return Image(data=img_bytes.getvalue(), format="png")
        
    except ImageError as e:
        raise McpError(str(e.message))
    except Exception as e:
        raise McpError(f"Error occurred while displaying image: {str(e)}") 