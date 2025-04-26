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

1. Configure Claude Desktop
   * Click on **Claude > Settings** from the Claude Desktop menu.
   * When the popup appears, select **Developer** from the left menu, and click the **Edit Settings** button.
   * This will open a folder containing the settings file. The name of this settings file is:
   * `claude_desktop_config.json`

<div align="center">
<img src="https://blog.kakaocdn.net/dn/bIl5q9/btsM3U5Vjw5/aGruWqP3wNmWZ1sKrnhbPk/img.png" width="70%">
</div>

3. Add the following content to the settings file (Python version):

   - python version

     ```json
     "nova-canvas": {
       "command": "uvx",
       "args": [
         "aws-nova-canvas-mcp"
       ],
       "env": {
         "AWS_PROFILE": "YOUR_AWS_PROFILE"
       }
     }
     ```

     > ✅ Only AWS_PROFILE is required. Other variables like AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, and PORT are optional and not necessary if your AWS profile is set correctly.
     >
     > ​	⚙️ If the setup is completed successfully, you can see that the "nova-canvas" item has been added in **Claude > Settings > Developer tab**.
     > ⚠️ **Important:** MCP settings only work on the **Claude desktop app, not the Claude web browser version**

## Image Save Location

By default, all generated or edited images will be saved in the following directory:

* **macOS / Linux**:  `~/Desktop/aws-nova-canvas`
* **Windows**:  `C:\Users\YourUsername\Desktop\aws-nova-canvas`

> 📁 If no image save path is specified, the application will automatically create and use the folder above.

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
