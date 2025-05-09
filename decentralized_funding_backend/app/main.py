from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Database
from app.core.auth import create_initial_admin
from app.routes import user_router, project_router, donation_router, auth, admin

# Initialize FastAPI app
app = FastAPI(
    title="Decentralized Funding API",
    description="API for decentralized crowdfunding platform",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await Database.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    Database.close_mongo_connection()

# Include routers
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(donation_router, prefix="/api/donations", tags=["donations"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}