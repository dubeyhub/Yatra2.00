import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    APP_NAME = "Yatra"
    TAGLINE = "Global Sacred Pilgrimages & Spiritual Journeys"
    SECRET_KEY = os.getenv("SECRET_KEY", "yatra-sacred-pilgrimage-secret-key-2026")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "yatra.db"))
    if not os.path.isabs(DATABASE_PATH):
        DATABASE_PATH = str(BASE_DIR / DATABASE_PATH)
    
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    TESTING = False
    
    # Currency configuration
    CURRENCY_SYMBOL = "₹"
    CURRENCY_CODE = "INR"
    
    # Global Countries
    FOCUS_COUNTRIES = [
        "India",
        "Nepal",
        "Vatican City",
        "Israel",
        "Saudi Arabia",
        "Japan",
        "Spain"
    ]
    
    # Standard states highlighted in religious focus (India)
    FOCUS_STATES = [
        "Uttar Pradesh",
        "Uttarakhand",
        "Gujarat",
        "Rajasthan",
        "Punjab",
        "Andhra Pradesh",
        "Tamil Nadu",
        "Maharashtra",
        "Bihar",
        "Odisha"
    ]
    
    # Destination Categories
    DESTINATION_CATEGORIES = [
        ("temple", "Temple / Shrine"),
        ("pilgrimage_route", "Pilgrimage Route / Circuit"),
        ("sacred_river", "Sacred River & Ghat"),
        ("mosque_dargah", "Mosque / Dargah"),
        ("church", "Church / Cathedral / Basilica"),
        ("gurudwara", "Gurudwara"),
        ("monastery", "Monastery / Zen Temple"),
        ("heritage_site", "Spiritual Heritage Site")
    ]
    
    # Religious Traditions
    RELIGIOUS_TRADITIONS = [
        "Hinduism",
        "Buddhism",
        "Sikhism",
        "Islam",
        "Christianity",
        "Judaism",
        "Shinto",
        "Jainism",
        "Interfaith / Multi-faith"
    ]
    
    # AI Chatbot Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Sample price disclaimer text
    SAMPLE_PRICE_DISCLAIMER = (
        "Note: Prices shown are verified sample estimates in INR (₹) or local equivalents for pilgrimage planning and budgeting purposes. "
        "Actual costs may vary by season, festivals, availability, and on-ground booking vendors."
    )

class TestConfig(Config):
    TESTING = True
    DATABASE_PATH = ":memory:"
    DEBUG = False
