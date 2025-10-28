from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

# MAILING_
FROM_MAIL = config('FROM_MAIL')
REVIEWER_MAILS = config('REVIEWER_MAILS', default='', cast=lambda v: [s.strip() for s in v.split(',')])
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
