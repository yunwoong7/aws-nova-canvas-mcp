<h2 align="center">
AWS Nova Canvas MCP Server
</h2>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python"/>
  <img src="https://img.shields.io/badge/Amazon-Bedrock-FF9900?logo=amazon&logoColor=white"/>
</div>

An MCP server that allows you to generate and edit images using the Nova Canvas model of Amazon Bedrock.

## Features

- Text to Image
- Image Inpainting
- Image Outpainting
- Image Variation
- Image Conditioning
- Color Guided Generation
- Background Removal
- Show Image Thumbnails

## Installation

### Claude Desktop Setup

1. Clone the repository
```bash
git clone https://github.com/yunwoong/aws-nova-canvas-mcp.git
```

2. Configure Claude Desktop
   * Click on **Claude > Settings** from the Claude Desktop menu.
   * When the popup appears, select **Developer** from the left menu, and click the **Edit Settings** button.
   * This will open a folder containing the settings file. The name of this settings file is:
   * `claude_desktop_config.json`

<div align="center">
<img src="https://blog.kakaocdn.net/dn/bIl5q9/btsM3U5Vjw5/aGruWqP3wNmWZ1sKrnhbPk/img.png" width="70%">
</div>

3. Add the following content to the settings file:

```json
"nova-canvas": {
  "command": "uv",
  "args": [
    "--directory",
    "Path to clone folder",
    "run",
    "src/server.py"
  ],
  "env": {
    "AWS_ACCESS_KEY_ID": "YOUR_AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY": "YOUR_AWS_SECRET_ACCESS_KEY",
    "AWS_REGION": "us-east-1",
    "PORT": "8000"
  }
}
```

5. Environment Variables Explanation
   - **Required**:
     - `AWS_ACCESS_KEY_ID`: AWS Access Key ID
     - `AWS_SECRET_ACCESS_KEY`: AWS Secret Key
     - `AWS_REGION`: AWS Region (default: `us-east-1`)

   - **Optional**:
     - `PORT`: Port number for the server (default: `8000`)
     - `IMAGES_DIR`: Path where generated images will be saved (default: `nova_canvas_images` folder in the user's home directory)
     - `BEDROCK_MODEL_ID`: Model ID to use (default: `amazon.nova-canvas-v1:0`)
   
   > ⚙️ If the setup is completed successfully, you can see that the "nova-canvas" item has been added in **Claude > Settings > Developer tab**.
   > ⚠️ **Important:** MCP settings only work on the **Claude desktop app, not the Claude web browser version**

<div align="center">
<img src="https://blog.kakaocdn.net/dn/bpUWLj/btsM4kJZC6v/HHQfQctKsevWnK6LCKEkv0/img.png" width="70%">
</div>

## Usage Example

<div align="center">
<img src="https://blog.kakaocdn.net/dn/uNi8L/btsM4pEjswV/hSfxo1gHzPvpXPsEEyuijk/img.gif" width="70%">
</div>

## Limitations

- Prompt text supports up to 1024 characters
- Image generation allows up to 3 images at a time
- Image variation requires 1-5 reference images
- Color guide supports 1-10 color codes

## License

MIT License
