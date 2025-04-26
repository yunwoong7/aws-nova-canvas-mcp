import base64
import json
from typing import Dict, Any

from mcp import McpError

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def inpainting(
        image_path: str,
        prompt: str,
        mask_prompt: str,
        negative_prompt: str = "",
        height: int = 512,
        width: int = 512,
        cfg_scale: float = 8.0,
        open_browser: bool = True,
        output_path: str = None,
) -> Dict[str, Any]:
    """
    Inpaint a specific part of an image using a text mask prompt.
    
    Args:
        image_path: File path of the original image
        prompt: Text prompt for the area to be inpainted
        mask_prompt: Text prompt for specifying the area to be masked (e.g., "window", "car")
        negative_prompt: Text prompt for excluding attributes from generation
        height: Output image height (pixels)
        width: Output image width (pixels)
        cfg_scale: Image matching degree for the prompt (1-20)
        open_browser: Whether to open the image in the browser after generation
        output_path: Absolute path to save the image
        
    Returns:
        Dict: Dictionary containing the file path of the inpainted image
    """
    try:
        # Read image file and encode to base64
        with open(image_path, "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "INPAINTING",
            "inPaintingParams": {
                "text": prompt,
                "negativeText": negative_prompt,
                "image": input_image,
                "maskPrompt": mask_prompt
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
        image_info = save_image(image_bytes, open_browser=open_browser, output_path=output_path)

        # Generate result
        result = {
            "image_path": image_info["image_path"],
            "message": f"Inpainting completed successfully. Saved location: {image_info['image_path']}"
        }

        return result

    except ImageError as e:
        raise McpError(str(e.message))
    except Exception as e:
        raise McpError(f"Error occurred while inpainting: {str(e)}")
