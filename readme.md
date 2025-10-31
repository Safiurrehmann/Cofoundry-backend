A FastAPI app that creates and deploys startup websites automatically using a local HTML template and AI.
The site can then be deployed directly to Vercel or Netlify.

🧩 Features

Generate full websites using AI and a base HTML template

Keeps your original CSS and JS intact

Deploys automatically to Vercel or Netlify

Simple FastAPI backend with CORS enabled

⚙️ Setup
1️⃣ Install dependencies
pip install -r requirements.txt


requirements.txt

fastapi==0.116.1
uvicorn==0.35.0
httpx==0.28.1
pydantic==2.11.7
python-multipart==0.0.20

2️⃣ Set environment variables
OPENAI_API_KEY=your_openai_key
NETLIFY_TOKEN=your_netlify_token
VERCEL_TOKEN=your_vercel_token

3️⃣ Run the server
uvicorn main:app --reload --port 8000

Server runs on 👉 http://127.0.0.1:8000

🧠 How It Works

Takes your startup info (name, tagline, CEO, etc.)

Fills that data into an existing templates/index.html

Saves the new website to generated_sites/{startup_name}

Deploys the site to Netlify or Vercel

🌐 Endpoints
POST /generate-website

Generates a website using the provided info.

Form fields:

startup_name

tagline

description

introduction

ceo_name

ceo_intro

email

sections (JSON array)

Example:

curl -X POST "http://127.0.0.1:8000/generate-website" \
-F "startup_name=Soventure" \
-F "tagline=Empowering Innovators" \
-F "sections=[\"Hero\",\"About\",\"Team\",\"Contact\"]"

POST /deploy/{startup_name}

Deploys the generated website to Vercel or Netlify.

Example:

curl -X POST "http://127.0.0.1:8000/deploy/Soventure"


Response:

{
  "message": "Deployment successful!",
  "url": "https://soventure.vercel.app"
}

📁 Folder Structure
project/
├── main.py
├── services/
│   ├── website_service.py
│   └── deploy_service.py
├── templates/
│   └── index.html
├── generated_sites/
│   └── Soventure/
└── requirements.txt

🧰 Notes

Templates stay untouched — new sites are saved separately.

Works asynchronously for faster performance.

Use valid API tokens before deploying.