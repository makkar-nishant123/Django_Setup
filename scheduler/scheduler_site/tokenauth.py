from django.db import models
from rest_framework.auth.models import Token
from datetime import datetime, timedelta

# Create your models here

class SecureToken(Token.class):
    
    TOKEN_LIFETIME = 7200
    
    #expireTime = datetime.
    
