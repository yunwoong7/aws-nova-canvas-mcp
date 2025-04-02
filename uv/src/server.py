import logging

from mcp.server.fastmcp import FastMCP

from src.config import get_app_config
from src.tools.background_removal import background_removal
from src.tools.color_guided_generation import color_guided_generation
from src.tools.image_conditioning import image_conditioning
from src.tools.image_variation import image_variation
from src.tools.inpainting import inpainting
from src.tools.outpainting import outpainting
from src.tools.text_to_image import text_to_image
from src.utils.image import get_image

# Set logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Get configuration
conf = get_app_config()

MODEL_ID = conf['model_id']

# Create MCP server
mcp = FastMCP("NovaCanvas Server", port=int(conf['port']))

# Register tools with names and descriptions
mcp.add_tool(text_to_image)
mcp.add_tool(inpainting)
mcp.add_tool(outpainting)
mcp.add_tool(image_variation)
mcp.add_tool(image_conditioning)
mcp.add_tool(color_guided_generation)
mcp.add_tool(background_removal)


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
    print("\n" + "=" * 50)
    print(f"MODEL_ID: {MODEL_ID}")
    print(f"Press Ctrl+C to exit.")
    print(f"Starting NovaCanvas server...")
    print("=" * 50 + "\n")

    mcp.run()


if __name__ == "__main__":
    main()
