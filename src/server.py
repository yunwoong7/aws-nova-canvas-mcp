import json
import logging
import base64

from mcp import McpError
from mcp.server.fastmcp import FastMCP

from config import get_app_config
from .exceptions import ImageError
from .utils.bedrock import generate_image
from .utils.image import get_image

# Set logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Get configuration
conf = get_app_config()

MODEL_ID = conf['model_id']

# Create MCP server
mcp = FastMCP("NovaCanvas Server", port=int(conf['port']))

# Import tools
from .tools import (
    text_to_image,
    inpainting,
    outpainting,
    image_variation,
    image_conditioning,
    color_guided_generation,
    background_removal,
    show_image
)

# Image resource processing
@mcp.resource("image://{image_id}")
async def image_resource(image_id: str) -> bytes:
    """
    Resource handler for image:// protocol
    
    Args:
        image_id: Image ID
        
    Returns:
        bytes: Image data
    """
    return await get_image(image_id)

def main():
    print("\n" + "="*50)
    print(f"MODEL_ID: {MODEL_ID}")
    print(f"Press Ctrl+C to exit.")
    print(f"Starting NovaCanvas server...")
    print("="*50 + "\n")

    mcp.run()

if __name__ == "__main__":
    main()