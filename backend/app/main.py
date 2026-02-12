from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import company_routes, job_routes, application_routes, candidate_routes, analytics_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic AI Hiring Platform",
    description="AI-powered talent evaluation system with explainable decisions",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Agentic AI Hiring Platform API",
        "version": "2.0",
        "features": [
            "AI-powered resume evaluation",
            "Skill extraction & matching",
            "Fraud detection",
            "Explainable AI (XAI) decisions",
            "Skill gap analysis",
            "Skill evidence graphs",
            "Candidate ranking",
            "Audit trail"
        ],
        "endpoints": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "health": "/health",
            "companies": "/company",
            "jobs": "/job",
            "applications": "/apply",
            "candidates": "/candidate",
            "analytics": "/analytics"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Agentic AI Hiring Platform",
        "version": "2.0.0"
    }

# Include routers
app.include_router(company_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router)
app.include_router(candidate_routes.router)
app.include_router(analytics_routes.router)
