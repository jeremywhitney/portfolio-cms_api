"""Helper code and fixtures that support pytest test execution."""

import os
import sys
import django
from django.conf import settings

# Add the project root directory to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfoliocmsproject.settings")
django.setup()
