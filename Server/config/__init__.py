import os

DOMAIN = None

SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
# Secret key for any 3-rd party libraries

SERVICE_NAME = 'Flask Serverless'

SWAGGER = {
    'title': SERVICE_NAME,
    'specs_route': '/docs/',
    'uiversion': 3,

    'info': {
        'title': SERVICE_NAME + ' API',
        'version': '1.0',
        'description': ''
    },

    'basePath': '/'
}
