from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Seguridad / Entorno
# =========================
# En Render define DJANGO_SECRET_KEY como variable de entorno.
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-cambia-esto-en-produccion"
)

# DEBUG: en tu PC puedes dejar DEBUG=1 en entorno, en Render pon DEBUG=0
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]


# =========================
# Apps
# =========================
INSTALLED_APPS = [
    'catalogo',
    'pacientes',
    'agenda',
    'espera',
    'cuentas',
    'rest_framework',
    'api',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ para estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'proyecto_odontologia.urls'


# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_odontologia.wsgi.application'


# =========================
# Base de datos
# =========================
# ✅ DEPLOY RÁPIDO EN RENDER: SQLite (evita caídas por MySQL local)
# Render suele exponer la variable RENDER. Si no estuviera, puedes usar IS_RENDER.
IS_RENDER = os.getenv("RENDER") is not None or os.getenv("IS_RENDER") == "1"

if IS_RENDER:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # ✅ LOCAL: MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'odontowait_db',
            'USER': 'odontowait_user',
            'PASSWORD': 'Odonto123*',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


# =========================
# Validación contraseñas
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =========================
# Idioma / zona horaria
# =========================
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# =========================
# Archivos estáticos
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Si tienes carpeta static local, déjala:
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================
# Login / sesiones
# =========================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'

SESSION_COOKIE_AGE = 30 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# =========================
# Seguridad (mínimo razonable)
# =========================
SECURE_CONTENT_TYPE_NOSNIFF = True

# En Django moderno, SECURE_BROWSER_XSS_FILTER ya no aporta mucho (es header viejo),
# pero no rompe. Si quieres, lo puedes quitar.
SECURE_BROWSER_XSS_FILTER = True

# Cookies secure: en Render (https) debería ser True, en local False
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG