import base64
import json
from typing import Dict, Any

from mcp import McpError

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def outpainting(
        image_path: str,
        mask_image_path: str,
        prompt: str,
        negative_prompt: str = "",
        outpainting_mode: str = "DEFAULT",
        height: int = 512,
        width: int = 512,
        cfg_scale: float = 8.0,
        output_path: str = None,
) -> Dict[str, Any]:
    """
    Expand the image to create an outpainting.
    
    Args:
        image_path: File path of the original image
        mask_image_path: File path of the mask image
        prompt: Text describing the content to be generated in the outpainting area
        negative_prompt: Text specifying attributes to exclude from generation
        outpainting_mode: Outpainting mode (DEFAULT or PRECISE)
        height: Output image height (pixels)
        width: Output image width (pixels)
        cfg_scale: Prompt matching degree (1-20)
        output_path: Absolute path to save the image
        
    Returns:
        Dict: Dictionary containing the file path of the outpainted image
    """
    try:
        # Validate outpainting mode
        if outpainting_mode not in ["DEFAULT", "PRECISE"]:
            raise ImageError("outpainting_mode must be 'DEFAULT' or 'PRECISE'.")

        # Read image file and encode to base64
        with open(image_path, "rb") as image_file:
            input_image = base64.b64encode(image_file.read()).decode('utf8')

        with open(mask_image_path, "rb") as mask_file:
            input_mask_image = base64.b64encode(mask_file.read()).decode('utf8')

        body = json.dumps({
            "taskType": "OUTPAINTING",
            "outPaintingParams": {
                "text": prompt,
                "negativeText": negative_prompt,
                "image": input_image,
                "maskImage": input_mask_image,
                "outPaintingMode": outpainting_mode
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
            "message": f"Outpainting completed successfully. Saved location: {image_info['image_path']}"
        }

        return result

    except Exception as e:
        raise McpError(f"Error occurred while outpainting: {str(e)}")
