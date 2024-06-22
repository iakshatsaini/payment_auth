import os
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./configuration/.env", override=True)
getenv = os.getenv

class config:
    APP_SECRET_KEY = getenv("APP_SECRET_KEY")
    OTP_AUTH_SECRET = getenv("OTP_AUTH_SECRET")
    
    TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = getenv("TWILIO_PHONE_NUMBER")
    
    STRIPE_SECRET_KEY = getenv("STRIPE_SECRET_KEY")
    CLIENT_ID = getenv("CLIENT_ID")
    CLIENT_SECRET = getenv("CLIENT_SECRET")
    
    STRIPE_PUBLISHABLE_KEY = getenv("STRIPE_PUBLISHABLE_KEY")