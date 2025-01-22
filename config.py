from datetime import timedelta

class Config:
    SECRET_KEY = "MY-SECRET-KEY" 
    JWT_EXP_DELTA = timedelta(minutes=30)
