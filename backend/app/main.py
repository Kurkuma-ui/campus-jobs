from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import router as auth_router
from .routers.vacancies import router as vacancies_router
from .routers.applications import router as applications_router

app = FastAPI(title="Campus Jobs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vacancies_router)
app.include_router(applications_router)

@app.get("/health")
def health():
    return {"status": "ok"}
