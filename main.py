from fastapi import HTTPException
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from services.website_service import generate_website
import os
from fastapi.middleware.cors import CORSMiddleware

import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for generated files
GENERATED_DIR = "generated_sites"
os.makedirs(GENERATED_DIR, exist_ok=True)

from fastapi import Form, File, UploadFile
import json
@app.post("/generate-website")
async def generate_website_route(
    startup_name: str = Form(...),
    tagline: str = Form(...),
    description: str = Form(...),
    introduction: str = Form(...),
    ceo_name: str = Form(...),
    ceo_intro: str = Form(...),
    email: str = Form(...),
    sections: str = Form(...)
):
    """
    Handles website generation with additional CEO and contact details.
    """
    try:
        selected_sections = json.loads(sections)

        result = await generate_website(
            startup_name=startup_name,
            tagline=tagline,
            description=description,
            introduction=introduction,
            ceo_name=ceo_name,
            ceo_intro=ceo_intro,
            email=email,
            sections=selected_sections
        )

        return result

    except Exception as e:
        logger.error(f"Error generating website: {e}")
        raise HTTPException(status_code=500, reason=str(e))



from services.deploy_service import deploy_to_netlify, deploy_to_vercel

@app.post("/deploy/{startup_name}")
async def deploy_route(startup_name: str):
    """
    Deploys the generated website to Netlify and returns its live URL.
    """
    try:
        result = await deploy_to_vercel(startup_name)
        return {"message": "Deployment successful!", "live_url": result["url"]}

    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Path to React build folder
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "dist")

# Serve static assets (JS/CSS/images)
app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_PATH, "assets")), name="assets")

# Serve index.html for all other routes (let React handle routing)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_file = os.path.join(FRONTEND_PATH, "index.html")
    return FileResponse(index_file)
