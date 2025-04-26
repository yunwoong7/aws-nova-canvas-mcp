import base64
import json
from typing import Dict, Any, List

from mcp import McpError

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def image_variation(
        image_paths: List[str],
        prompt: str = "",
        negative_prompt: str = "",
        similarity_strength: float = 0.7,
        height: int = 512,
        width: int = 512,
        cfg_scale: float = 8.0,
        output_path: str = None,
) -> Dict[str, Any]:
    """
    Generate a new variation of the input image while maintaining its content.
    
    Args:
        image_paths: List of file paths of the original images (1-5)
        prompt: Text for generating a variation image (optional)
        negative_prompt: Text specifying attributes to exclude from generation
        similarity_strength: Similarity between the original image and the generated image (0.2-1.0)
        height: Output image height (pixels)
        width: Output image width (pixels)
        cfg_scale: Prompt matching degree (1-20)
        output_path: Absolute path to save the image
        
    Returns:
        Dict: Dictionary containing the file path of the variation image
    """
    try:
        # Validate image paths
        if len(image_paths) < 1 or len(image_paths) > 5:
            raise ImageError("image_paths list must contain 1-5 images.")

        if similarity_strength < 0.2 or similarity_strength > 1.0:
            raise ImageError("similarity_strength must be between 0.2 and 1.0.")

        # Read image files and encode to base64
        encoded_images = []
        for img_path in image_paths:
            with open(img_path, "rb") as image_file:
                encoded_images.append(base64.b64encode(image_file.read()).decode('utf8'))

        body = json.dumps({
            "taskType": "IMAGE_VARIATION",
            "imageVariationParams": {
                "text": prompt,
                "negativeText": negative_prompt,
                "images": encoded_images,
                "similarityStrength": similarity_strength,
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
            "message": f"Image variation completed successfully. Saved location: {image_info['image_path']}"
        }

        return result

    except Exception as e:
        raise McpError(f"Error occurred while image variation: {str(e)}")
