from .base import *
import os
from decouple import config

env = config('ENV_NAME')

if env == 'production':
    from .production import *
elif env == 'local':
    from .local import *
elif env == 'staging':
    from .staging import *
else:
    print('No environment chosen!')
