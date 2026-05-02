# FastAPI + MySQL Sample Project
# uvicorn app.main:app --reload 
# http://127.0.0.1:8000/home-deals
# http://127.0.0.1:8000/home-mobiles

Copy `.env.example` to `.env` and set `DATABASE_URL`.

Install:
    python -m pip install -r requirements.txt

Run:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API:
- GET /products
- GET /products/{id}
- GET /raw-query