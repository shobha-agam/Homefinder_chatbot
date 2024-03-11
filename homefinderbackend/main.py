import uvicorn
from fastapi import FastAPI
from app.models import auth_model
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import auth_router
from app.routes.owner_routes import chatbot_router
from app.routes.user_routes import user_router
from app.models import chatbot_model
from app.config.db_config import engine
from app.routes.admin_routes import admin_router

app= FastAPI(
    docs_url="/chatbot/docs",
    title="HomeFinder",
    description="HomeFinder chatbot is designed to find a Flat/PG/Hostels.",
    version="1.0",
    openapi_url="/homefinder/openapi.json"
)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["HomeFinder default page"])
async def home():
    return{
       "msg": "Welcome to HomeFinder"
    }

app.include_router(auth_router, tags=["HomeFinder Auth Routes"])
app.include_router(chatbot_router, tags=["HomeFinder Owner Routes"])
app.include_router(user_router, tags=["HomeFinder User Routes"])
app.include_router(admin_router, tags=["HomeFinder Admin Routes"])

auth_model.Base.metadata.create_all(bind=engine)
chatbot_model.Base.metadata.create_all(bind=engine)

if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
