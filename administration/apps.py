# from django.apps import AppConfig


# class AdministrationConfig(AppConfig):
#     name = 'administration'


import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "administration"
    verbose_name = _("Administration")

    def ready(self):
        importlib.import_module("administration.receivers")