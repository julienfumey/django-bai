from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

STATIC_ROOT = config('STATIC_ROOT')

# MAILING_
FROM_MAIL = config('FROM_MAIL')
REVIEWER_MAILS = config('REVIEWER_MAILS', default='', cast=lambda v: [s.strip() for s in v.split(',')])
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='127.0.0.1')
EMAIL_PORT = config('EMAIL_PORT', default='')
