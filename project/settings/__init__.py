from .base import *
from .django_elastic import *
try:
    from .local import *
except ImportError:
    pass

