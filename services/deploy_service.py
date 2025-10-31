import base64
import os
import tempfile
import zipfile
import httpx
import logging
import random
import string

# ───────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

NETLIFY_TOKEN = ""
NETLIFY_API = "https://api.netlify.com/api/v1/sites"


# ───────────────────────────────────────────────────────────────
# UTILITIES
# ───────────────────────────────────────────────────────────────
def generate_unique_name(base_name: str, length: int = 5):
    """Generate a unique Netlify site name."""
    base = base_name.lower().replace(" ", "-")
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{base}-{rand_suffix}"


async def create_site(site_name: str):
    """Create a new Netlify site with a unique name."""
    headers = {
        "Authorization": f"Bearer {NETLIFY_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"name": site_name}

    async with httpx.AsyncClient() as client:
        response = await client.post(NETLIFY_API, headers=headers, json=payload)

    # Handle duplicate names
    if response.status_code == 422:
        logger.warning(f"⚠️ Site name '{site_name}' already exists. Retrying with new name...")
        new_name = generate_unique_name(site_name)
        return await create_site(new_name)

    if response.status_code != 201:
        raise Exception(f"❌ Failed to create site: {response.text}")

    site = response.json()
    logger.info(f"✅ Site created: {site['name']} ({site['id']})")
    return site["id"], site


# ───────────────────────────────────────────────────────────────
# DEPLOY FUNCTION
# ───────────────────────────────────────────────────────────────
async def deploy_to_netlify(startup_name: str):
    """
    Deploys exactly 3 files: index.html, styles.css, script.js
    All files are expected in: generated_sites/{startup_name}/
    """
    folder_path = os.path.join("generated_sites", startup_name)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"❌ Folder not found: {folder_path}")

    logger.info(f"🚀 Creating new site for {startup_name}...")
    site_id, site_info = await create_site(startup_name)  # your existing function

    # Collect only specific files
    target_files = ["index.html", "styles.css", "script.js"]
    existing_files = [f for f in target_files if os.path.exists(os.path.join(folder_path, f))]

    if not existing_files:
        raise Exception("❌ No valid files found to upload.")

    # 🗜️ Create a temporary ZIP
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
        with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in existing_files:
                file_path = os.path.join(folder_path, filename)
                zipf.write(file_path, arcname=filename)
                logger.info(f"📦 Added {filename} to ZIP")
        zip_path = tmp_zip.name

    deploy_url = f"{NETLIFY_API}/{site_id}/deploys"
    headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

    async with httpx.AsyncClient() as client:
        with open(zip_path, "rb") as f:
            files = {"file": (f"{startup_name}.zip", f, "application/zip")}
            response = await client.post(deploy_url, headers=headers, files=files)

    os.remove(zip_path)  # clean up temp file

    if response.status_code not in (200, 201):
        raise Exception(f"❌ Failed to deploy site: {response.text}")

    deploy_data = response.json()
    deploy_url_final = deploy_data.get("deploy_ssl_url") or deploy_data.get("url")

    logger.info(f"✅ Deployment successful! 🌐 {deploy_url_final}")

    return {
        "startup_name": startup_name,
        "site_name": site_info["name"],
        "url": deploy_url_final
    }

from dotenv import load_dotenv
load_dotenv(override=True)

VERCEL_API = "https://api.vercel.com/v13/deployments"
VERCEL_TOKEN =os.getenv("VERCEL_TOKEN")
VERCEL_TEAM_ID = None  # optional, only if you use a Vercel team


async def deploy_to_vercel(startup_name: str):
   
    """
    Deploys the folder generated_sites/{startup_name}/ to Vercel.
    Includes index.html, styles.css, script.js and any other files in the folder.
    """
    folder_path = os.path.join("generated_sites", startup_name)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"❌ Folder not found: {folder_path}")

    logger.info(f"🚀 Deploying {startup_name} to Vercel...")

    # Collect all files in folder (recursively)
    files_payload = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            with open(full_path, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf-8")
            files_payload.append({
                "file": relative_path,
                "data": content,
                "encoding": "base64"
            })

    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": startup_name.lower(),
        "projectSettings": {
            "framework": None
        },
        "files": files_payload
    }

    if VERCEL_TEAM_ID:
        payload["target"] = "production"
        params = {"teamId": VERCEL_TEAM_ID}
    else:
        params = {}

    async with httpx.AsyncClient() as client:
        response = await client.post(VERCEL_API, headers=headers, json=payload, params=params)

    if response.status_code not in (200, 201):
        raise Exception(f" Failed to deploy: {response.text}")

    deploy_data = response.json()
    url = deploy_data.get("url")

    if not url.startswith("https://"):
        url = f"https://{url}"

    logger.info(f"✅ Deployment successful! 🌐 {url}")

    return {
        "startup_name": startup_name,
        "url": url
    }