import base64
import json
from typing import Dict, Any, List, Optional

from mcp import McpError
from mcp.server.fastmcp import Context

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def color_guided_generation(
        prompt: str,
        colors: List[str],
        reference_image_path: Optional[str] = None,
        negative_prompt: str = "",
        height: int = 512,
        width: int = 512,
        cfg_scale: float = 8.0,
        output_path: str = None,
        ctx: Context = None,
) -> Dict[str, Any]:
    """
    Generate an image using a specified color palette.
    
    Args:
        prompt: Text describing the image to be generated
        colors: List of color codes (1-10 hex color codes, e.g., "#ff8080")
        reference_image_path: File path of the reference image (optional)
        negative_prompt: Text specifying attributes to exclude from generation
        height: Output image height (pixels)
        width: Output image width (pixels)
        cfg_scale: Prompt matching degree (1-20)
        output_path: Absolute path to save the image
        ctx: MCP context
        
    Returns:
        Dict: Dictionary containing the file path of the generated image
    """
    try:
        # Validate color list
        if len(colors) < 1 or len(colors) > 10:
            raise ImageError("colors list must contain 1-10 color codes.")

        # Validate color codes
        for color in colors:
            if not color.startswith("#") or len(color) != 7:
                raise ImageError(f"Invalid color code: {color}. Hex color codes must be in the format '#rrggbb'.")

        params = {
            "text": prompt,
            "negativeText": negative_prompt,
            "colors": colors
        }

        # If reference image exists, add it
        if reference_image_path:
            with open(reference_image_path, "rb") as image_file:
                input_image = base64.b64encode(image_file.read()).decode('utf8')
                params["referenceImage"] = input_image

        body = json.dumps({
            "taskType": "COLOR_GUIDED_GENERATION",
            "colorGuidedGenerationParams": params,
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": height,
                "width": width,
                "cfgScale": cfg_scale
            }
        })

        # Generate image
        image_bytes = generate_image(body)

        # Save image
        image_info = save_image(image_bytes, output_path=output_path)

        # Generate result
        result = {
            "image_path": image_info["image_path"],
            "message": f"Image generated successfully using color palette. Saved location: {image_info['image_path']}"
        }

        return result

    except Exception as e:
        raise McpError(f"Error occurred while generating image using color palette: {str(e)}")
