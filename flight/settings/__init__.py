"""Entry point of the application"""
import os

from .base import *

env_name = os.getenv('ENV_NAME', 'development')

if env_name == 'production':
    from .production import *
else:
    from .development import *
