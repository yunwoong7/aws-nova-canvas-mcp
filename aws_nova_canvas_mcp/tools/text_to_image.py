import json
from typing import Dict, Any

from mcp import McpError

from ..exceptions import ImageError
from ..utils.bedrock import generate_image
from ..utils.image_storage import save_image


async def text_to_image(
        prompt: str,
        negative_prompt: str = "",
        height: int = 1024,
        width: int = 1024,
        num_images: int = 1,
        cfg_scale: float = 8.0,
        seed: int = 0,
        open_browser: bool = True,
        output_path: str = None,
) -> Dict[str, Any]:
    """
    Generate an image from a text prompt. If a color palette is specified, use the color_guided_generation tool first.
    
    Args:
        prompt: Text prompt for generating an image (maximum 1024 characters)
        negative_prompt: Text prompt for excluding attributes from generation (maximum 1024 characters)
        height: Image height (pixels)
        width: Image width (pixels)
        num_images: Number of images to generate (maximum 4)
        cfg_scale: Image matching degree for the prompt (1-20)
        seed: Seed value for image generation
        open_browser: Whether to open the image in the browser after generation
        output_path: Absolute path to save the image
        
    Returns:
        Dict: Dictionary containing the file path of the generated image and the thumbnail image
    """
    try:
        # Validate prompt length
        if len(prompt) > 1024:
            raise ImageError("Prompt cannot exceed 1024 characters.")
        if len(negative_prompt) > 1024:
            raise ImageError("Negative prompt cannot exceed 1024 characters.")

        if num_images < 1 or num_images > 4:
            raise ImageError("num_images must be between 1 and 4.")

        body = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt,
                "negativeText": negative_prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": num_images,
                "height": height,
                "width": width,
                "cfgScale": cfg_scale,
                "seed": seed
            }
        })

        # Generate image
        image_bytes = generate_image(body)

        # Save image
        image_info = save_image(image_bytes, open_browser=open_browser, output_path=output_path)

        # Generate result
        result = {
            "image_path": image_info["image_path"],
            "message": f"Image generated successfully. Saved location: {image_info['image_path']}"
        }

        return result

    except Exception as e:
        raise McpError(f"Error occurred while generating image: {str(e)}")
