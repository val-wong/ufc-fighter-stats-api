# UFC Fighter Stats API 👊

A FastAPI-powered REST API that serves statistical data about UFC fighters. Built for portfolio demonstration purposes and hosted via Render.

---

![GitHub repo size](https://img.shields.io/github/repo-size/val-wong/ufc-fighter-stats-api)
![GitHub issues](https://img.shields.io/github/issues/val-wong/ufc-fighter-stats-api)
![GitHub last commit](https://img.shields.io/github/last-commit/val-wong/ufc-fighter-stats-api)
![CI](https://github.com/val-wong/ufc-fighter-stats-api/actions/workflows/deploy.yml/badge.svg)

---

## 📁 Folder Structure

```
UFC_Stats_API/
├── .env                  # Environment variables (excluded from version control)
├── .gitignore
├── README.md
├── render.yml            # Render deployment config
├── requirements.txt
├── data/
│   └── ufc_fighters_stats.csv
├── tests/
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── deploy.yml
└── ufc_api/
    └── main.py           # FastAPI app
```

## 🚀 Features

- Serve full dataset of UFC fighters via `/fighters`
- Lookup fighters by name with `/fighters/{name}`
- Supports sorting, searching, and filtering
- API key authentication
- CI/CD pipeline via GitHub Actions
- Deployment ready for Render.com

## 🧪 Running Locally

### 1. Clone & Create Virtual Environment
```bash
git clone https://github.com/val-wong/ufc-fighter-stats-api.git
cd ufc-fighter-stats-api
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable
Create a `.env` file:
```
UFC_API_KEY=your_api_key_here
```

### 4. Start the API
```bash
uvicorn ufc_api.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to explore the Swagger UI.

## 🌍 Deployment (Render)
Render deploys automatically via `render.yml`. On push to `main`, it:

- Installs dependencies
- Starts the FastAPI server
- Uses the API key from environment variables in the Render dashboard

## 🔐 Authentication
All endpoints (except `/`) require an API key via query parameter or header:
```bash
GET /fighters?api_key=your_api_key_here
```

## ✅ Testing
```bash
pytest
```

## 📬 API Endpoints Summary
- `/` → Welcome message
- `/fighters` → Get all fighters
- `/fighters/{name}` → Get stats by fighter name
- (Additional endpoints in progress...)

## 🛠 Tech Stack
- Python 3.11
- FastAPI
- Pandas
- Uvicorn
- GitHub Actions (CI/CD)
- Render (Hosting)

## 🧠 Why This Project?
This was created as a portfolio API project to demonstrate:
- API development with FastAPI
- Handling real-world data
- Securing endpoints
- CI/CD practices
- Modern deployment to the cloud

## 📸 Screenshots
(Coming soon — Postman demo + Swagger docs screenshots)

## 🙌 Contributions
PRs welcome — especially for tests, validation, or extra endpoints!

## 📄 License
MIT

---

_Developed with 💥 by [Val Wong](https://github.com/val-wong)_
