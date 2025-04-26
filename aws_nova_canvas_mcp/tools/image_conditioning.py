import base64
import json
from typing import Dict, Any

from mcp import McpError

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def image_conditioning(
        image_path: str,
        prompt: str,
        negative_prompt: str = "",
        control_mode: str = "CANNY_EDGE",
        height: int = 512,
        width: int = 512,
        cfg_scale: float = 8.0,
        output_path: str = None,
) -> Dict[str, Any]:
    """
    Generate an image that follows the layout and composition of a reference image.
    
    Args:
        image_path: File path of the reference image
        prompt: Text describing the image to be generated
        negative_prompt: Text specifying attributes to exclude from generation
        control_mode: Control mode (CANNY_EDGE, etc.)
        height: Output image height (pixels)
        width: Output image width (pixels)
        cfg_scale: Prompt matching degree (1-20)
        output_path: Absolute path to save the image
        
    Returns:
        Dict: Dictionary containing the file path of the generated image
    """
    try:
        # Read image file and encode to base64
        with open(image_path, "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": negative_prompt,
                "conditionImage": input_image,
                "controlMode": control_mode
            },
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
            "message": f"Image conditioning completed successfully. Saved location: {image_info['image_path']}"
        }

        return result

    except Exception as e:
        raise McpError(f"Error occurred while image conditioning: {str(e)}")
