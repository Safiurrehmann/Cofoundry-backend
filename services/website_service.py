import os
import base64
import json
import shutil
from fastapi import UploadFile
import httpx
import logging

logger = logging.getLogger(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEMPLATES_DIR = "templates"
GENERATED_DIR = "generated_sites"

async def generate_website(
    startup_name: str,
    tagline: str,
    description: str,
    introduction: str,
    ceo_name: str,
    ceo_intro: str,
    email: str,
    sections: list
):
    """
    Uses AI to fill an existing local HTML template with startup information,
    including CEO and contact details. Keeps original files intact and copies
    assets to a generated folder.
    """

    logger.info(f"🚀 Generating website from template for: {startup_name}")

    # ✅ Step 1: Define paths
    template_html_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(template_html_path):
        raise FileNotFoundError(f"Template not found at {template_html_path}")

    # Read the original template
    with open(template_html_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # ✅ Step 2: Build the OpenAI prompt
    prompt_text = f"""
You are an expert front-end developer and website designer.

You are given a ready-made HTML template. 
Your job is to **insert the following startup, CEO, and contact information**
naturally into the template while preserving all structure, styling, and
links to CSS or JS files.

Make sure the website looks professional and well-structured.
Use the given information to fill or adapt appropriate sections 
like Hero, About, Team, and Contact where relevant.

The contact section should clearly display the provided email address for communication.

Do not remove or rename <link>, <script>, or any class names.

Startup Info:
- Name: {startup_name}
- Tagline: {tagline}
- Description: {description}
- Introduction: {introduction}
- CEO Name: {ceo_name}
- CEO Introduction: {ceo_intro}
- Contact Email: {email}
- Sections to include or emphasize: {sections}

Return only the final valid HTML (no markdown, no code fences).

Here is the HTML template:
{template_html}
"""

    # ✅ Step 3: Call OpenAI API
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an expert HTML designer."},
                    {"role": "user", "content": prompt_text},
                ],
            },
        )

    if response.status_code != 200:
        logger.error(f"❌ OpenAI API error: {response.status_code} - {response.text}")
        raise Exception(f"Failed to generate website: {response.text}")

    html_content = response.json()["choices"][0]["message"]["content"]

    # ✅ Step 4: Create output directory
    output_dir = os.path.join(GENERATED_DIR, startup_name.replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Step 5: Copy assets (CSS, JS, etc.)
    for item in os.listdir(TEMPLATES_DIR):
        src_path = os.path.join(TEMPLATES_DIR, item)
        dest_path = os.path.join(output_dir, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        elif item != "index.html":
            shutil.copy2(src_path, dest_path)

    # ✅ Step 6: Write AI-modified HTML to the new folder
    output_html_path = os.path.join(output_dir, "index.html")
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    logger.info(f"✅ Website generated successfully at {output_html_path}")

    # ✅ Step 7: Return structured result
    return {
        "message": f"Website generated successfully for {startup_name}",
        "index_file": output_html_path,
        "html_preview": html_content[:1000],
        "ceo_name": ceo_name,
        "ceo_intro": ceo_intro,
        "email": email
    }


async def generate_logo(startup_name: str) -> str:
    """
    Generates a logo using OpenAI image API and saves it as a PNG.
    """
    logo_dir = os.path.join(GENERATED_DIR, startup_name)
    os.makedirs(logo_dir, exist_ok=True)
    logo_path = os.path.join(logo_dir, "logo.png")

    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-image-1",
                "prompt": f"Logo design for tech startup '{startup_name}', minimalistic and professional.",
                "size": "512x512",
            },
        )

    image_b64 = resp.json()["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_b64)

    with open(logo_path, "wb") as f:
        f.write(image_bytes)

    return logo_path
