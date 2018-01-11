from flask import Flask
from flasgger import Swagger

from app.docs import TEMPLATE
from app.views import ViewInjector

swagger = Swagger(template=TEMPLATE)
# To Swagger UI

view = ViewInjector()
# To Swagger Documentation


def create_app(config_name='dev'):
    """
    Creates Flask instance & initialize

    :rtype: Flask
    """
    config_path = '../config/{}.py'.format(config_name)
    # 인자로 config path를 통쨰로 넘겨주는 것보다 이상적

    app_ = Flask(__name__)
    app_.config.from_pyfile(config_path)

    swagger.init_app(app_)
    view.init_app(app_)

    return app_


app = create_app()
