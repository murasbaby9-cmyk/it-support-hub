import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
SECRET_KEY=os.environ['SECRET_KEY']
DEBUG=os.getenv('DEBUG','False').lower()=='true'
ALLOWED_HOSTS=[x.strip() for x in os.getenv('ALLOWED_HOSTS','').split(',') if x.strip()]
INSTALLED_APPS=['django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','tickets']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
if os.getenv('DATABASE_URL'): DATABASES['default']=dj_database_url.parse(os.environ['DATABASE_URL'])
LANGUAGE_CODE='kk'
TIME_ZONE='Asia/Almaty'
USE_TZ=True
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGGING={'version':1,'disable_existing_loggers':False,'formatters':{'standard':{'format':'{asctime} {levelname} {name} {message}','style':'{'}},'handlers':{'console':{'class':'logging.StreamHandler','formatter':'standard'}},'loggers':{'tickets':{'handlers':['console'],'level':'INFO','propagate':False},'django.security.DisallowedHost':{'handlers':['console'],'level':'ERROR','propagate':False}}}
INSTALLED_APPS.insert(0,'django.contrib.admin')
LANGUAGE_CODE='ru'
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
    CSRF_TRUSTED_ORIGINS=['https://'+os.environ['RENDER_EXTERNAL_HOSTNAME']]
    SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
