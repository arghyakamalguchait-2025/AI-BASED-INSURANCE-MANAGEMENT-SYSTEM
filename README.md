# InsureWise AI

InsureWise AI is a Flask-based insurance management system designed for demonstration and learning. It includes customer authentication, policy browsing, premium estimation, claim management, and an AI-powered insurance chatbot with a rule-based fallback.

## Features

- Customer registration and login
- Role-based admin access
- Insurance plan catalog with fictional data
- Recommendation engine and premium calculator
- Policy application flow
- Customer claims dashboard
- Administrator review tools
- InsureBot AI chatbot with rule-based fallback and Ollama support

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and update the values if needed.
4. Initialize the database and seed sample plans:
   ```bash
   python scripts/seed_database.py
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in a browser.

The application stores SQLite data in `instance/insurance.db`, resolved from
the project directory. Application startup creates missing tables and demo
records without deleting existing accounts, policies, claims, or plans.

## Admin Account

To create an admin account:

```bash
flask --app app create-admin
```

## Testing

```bash
python -m pytest -q
```

## Notes

- This project uses fictional insurance plans and sample data only.
- The chatbot tries to use Ollama if available and falls back to a rule-based reply when the model is unavailable.
