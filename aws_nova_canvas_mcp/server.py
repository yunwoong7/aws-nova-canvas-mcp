import logging
import os

from mcp.server.fastmcp import FastMCP

from .config import get_app_config
from .tools.background_removal import background_removal
from .tools.color_guided_generation import color_guided_generation
from .tools.image_conditioning import image_conditioning
from .tools.image_variation import image_variation
from .tools.inpainting import inpainting
from .tools.outpainting import outpainting
from .tools.text_to_image import text_to_image

# Set logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Get configuration
conf = get_app_config()

MODEL_ID = conf['model_id']

# Create MCP server
mcp = FastMCP("NovaCanvas Server", port=int(conf['port']))

# Register tools with names and descriptions
mcp.add_tool(text_to_image, 
             "text_to_image", 
             """Generate an image from a text prompt using aws nova canvas model. 
             If a color palette is specified, use the color_guided_generation tool first.""")
# mcp.add_tool(inpainting)
# mcp.add_tool(outpainting)
# mcp.add_tool(image_variation)
# mcp.add_tool(image_conditioning)
mcp.add_tool(color_guided_generation)
mcp.add_tool(background_removal)




def main():
    print("\n" + "=" * 50)
    print(f"MODEL_ID: {MODEL_ID}")
    print(f"Press Ctrl+C to exit.")
    print(f"Starting NovaCanvas server...")
    print("=" * 50 + "\n")

    mcp.run()


if __name__ == "__main__":
    main()
