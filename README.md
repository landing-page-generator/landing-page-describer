# Landing Page Describer

Help you to formulate requirements to your landing page

Hacked on [Sundai](https://sundai.club), Sep 15, 2024

# Installation

```bash
cp .env.example .env
nano .env
# then add your Gemini secret keys to the .env file
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run

## Local server

```bash
python main.py
```

or 

```bash
uvicorn main:app --reload
```

# Production deployment  

Auto deployed to Vercel https://landing-page-describer.vercel.app at each commit to `main` branch.
