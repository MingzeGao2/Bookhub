import os

PROJECT_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

print PROJECT_DIR
print PROJECT_PATH

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'staticfiles'),
)
