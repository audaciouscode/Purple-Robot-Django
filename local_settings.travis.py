import sys

SECRET_KEY = '_!4k)7rg*v1+%i!n=6f)8!l@j_jdan121vq(q*z14ovb390+cp'

ADMINS = [('Chris Karr', 'chris@audacious-software.com')]
ALLOWED_HOSTS = [ 'purple-robot.audacious-software.com' ]

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'purple_robot',
        'USER':     'purple_robot',
        'PASSWORD': 'MgzcoRNtg72f5ADP',
        'HOST':     'localhost',
        'PORT':     '',
    }
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'purple_robot_test',
            'USER':     'purple_robot',
            'PASSWORD': 'MgzcoRNtg72f5ADP',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
