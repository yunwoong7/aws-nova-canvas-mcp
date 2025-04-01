import json
import base64
from typing import Dict, Any
from ..server import mcp, generate_image, ImageError, McpError
from ..utils.image_storage import save_image
from mcp.server.fastmcp import Context

@mcp.tool()
async def background_removal(
    image_path: str,
    output_path: str = None,
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Remove the background of an image automatically.
    
    Args:
        image_path: File path of the original image
        output_path: Optional specific path to save the image
        ctx: MCP context
        
    Returns:
        Dict: Dictionary containing the file path of the image with the background removed
    """
    try:
        # Read image file and encode to base64
        with open(image_path, "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')
        
        body = json.dumps({
            "taskType": "BACKGROUND_REMOVAL",
            "backgroundRemovalParams": {
                "image": input_image,
            }
        })
        
        # Generate image
        image_bytes = generate_image(body)
        
        # Save image
        image_info = save_image(image_bytes, output_path=output_path)
        
        # Generate result
        result = {
            "image_path": image_info["image_path"],
            "message": f"Background removed successfully. Saved location: {image_info['image_path']}"
        }
        
        return result
        
    except ImageError as e:
        raise McpError(str(e.message))
    except Exception as e:
        raise McpError(f"Error occurred while removing background: {str(e)}") 