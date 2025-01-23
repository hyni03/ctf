from datetime import timedelta

class Config:
    SECRET_KEY = "MY-SECRET-KEY" 
    FLAG = "flag=\"ldULUFMR09SSVRITV9OT05FLUlTLURBTkdFUk9VUw==\""
    JWT_EXP_DELTA = timedelta(minutes=30)
