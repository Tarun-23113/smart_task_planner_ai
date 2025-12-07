from fastapi import FastAPI
from app.route.plan import plan_router
from app.database import Base, engine

app = FastAPI(title="Smart Task Planner")

Base.metadata.create_all(bind=engine)

app.include_router(plan_router)

@app.get("/")
def root():
    return {"message": "backend is running"}
