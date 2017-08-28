"""
BaseController

this module contains the BaseController class. This class
is a base wrapper of Flask Blueprint, making it easier to
modularize endpoints
"""

from flask import Blueprint


class BaseController(Blueprint):

    def __init__(self, name=__name__, **kwargs):
        """
        Bind controller to application with specified preffix.
        :param app: application
        :param preffix: preffix
        :param kwargs: parameters for app.register_blueprint than preffix
        """

        super().__init__(name, name, **kwargs)

        self.register_error_handler(404, self.handle_404)

    def handle_404(self, _):
        return dict(message='Requested page not found'), 404
