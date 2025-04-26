import base64
import json
from typing import Dict, Any

from mcp import McpError
from mcp.server.fastmcp import Context

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def background_removal(
        image_path: str,
        output_path: str = None,
        ctx: Context = None,
) -> Dict[str, Any]:
    """
    Remove the background of an image automatically.
    
    Args:
        image_path: File path of the original image, Please use the actual local file path where the image is stored.
        output_path: Absolute path to save the image
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

    except Exception as e:
        raise McpError(f"Error occurred while removing background: {str(e)}")
