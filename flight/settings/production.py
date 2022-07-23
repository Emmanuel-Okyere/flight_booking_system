"""Production settings"""
import os
from .base import *

DEBUG = True
ADMINS = (
('Gyateng Emmanuel', 'gyateng94@gmail.com'),
)
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DATABASE_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_DATABASE_PASSWORD'),
        'HOST': os.getenv('POSTGRES_DATABASE_HOST'),
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}
