A FastAPI app that creates and deploys startup websites automatically using a local HTML template and AI.
The sites can be deployed directly to Vercel or Netlify.

⚙️ Setup
pip install -r requirements.txt


requirements.txt

fastapi==0.116.1
uvicorn==0.35.0
httpx==0.28.1
pydantic==2.11.7
python-multipart==0.0.20


Set environment variables:

OPENAI_API_KEY=your_openai_key
NETLIFY_TOKEN=your_netlify_token
VERCEL_TOKEN=your_vercel_token


Run the server:

uvicorn main:app --reload --port 8000

🌐 API Endpoints

POST /generate-website
Generates a website using startup info and saves it to generated_sites/{startup_name}.

POST /deploy/{startup_name}
Deploys the generated site to Vercel or Netlify.

📁 Structure
project/
├── main.py
├── services/
│   ├── website_service.py
│   └── deploy_service.py
├── templates/
│   └── index.html
├── generated_sites/
└── requirements.txt