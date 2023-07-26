import connexion

def create_app(settings_override=None):
    """
    Create a Connexion application using the app factory pattern.

    :param settings_override: Override settings
    :return: Connexion app
    """

    api = connexion.FlaskApp(__name__, specification_dir="./swagger")
    api.add_api("swagger.yml")
    api.app.config.from_object("config.settings")

    if settings_override:
        api.app.config.update(settings_override)

    return api.app


def register_extensions(app):
    """
    Register extensions for the Flask application.

    :param app: Flask application instance
    :return: None
    """


