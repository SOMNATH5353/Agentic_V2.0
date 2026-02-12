import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
# Render provides DATABASE_URL, but we need to handle both postgres:// and postgresql://
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for Render: Convert postgres:// to postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# HuggingFace API Configuration
HF_API_KEY = os.getenv("HF_API_KEY")

# Fraud Detection Configuration
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.90))

# Environment Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required environment variables
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY environment variable is required")

